from dataclasses import dataclass
from datetime import date
from uuid import UUID

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


@dataclass(frozen=True, slots=True)
class MoviesResponse:
    """Модель выходных данных по фильмам."""

    id: UUID
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    genres: list[str]
    actors: list[str]
    directors: list[str]
    writers: list[str]


class MoviesApiMixin:
    """Миксин модель api для фильмов."""

    model = Filmwork
    http_method_names = ['get']

    def _agg_person(self, role: str) -> ArrayAgg:  # noqa
        return ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role__exact=role))

    def get_queryset(self) -> QuerySet:
        return (
            self.model.objects.prefetch_related(
                'genres',
                'person',
            )
            .values()
            .annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=self._agg_person(PersonFilmwork.RoleType.ACTOR.value),
                directors=self._agg_person(PersonFilmwork.RoleType.DIRECTOR.value),
                writers=self._agg_person(PersonFilmwork.RoleType.WRITER.value),
            )
            .values(
                'id',
                'title',
                'description',
                'creation_date',
                'rating',
                'type',
                'genres',
                'actors',
                'directors',
                'writers',
            )
            .order_by('title')
        )

    def render_to_response(self, context, **response_kwargs) -> JsonResponse:  # noqa
        return JsonResponse(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Модель api для детальной информации по фильму."""

    def get_context_data(self, **kwargs) -> MoviesResponse:
        return super().get_context_data(**kwargs)['object']


class MoviesListApi(MoviesApiMixin, BaseListView):
    """Модель api для информации по фильмам."""

    paginate_by: int = 50

    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, int | None | list[MoviesResponse]]:
        queryset = self.get_queryset()

        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
