from typing import Any

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    @staticmethod
    def _aggregate_person(role: Any) -> ArrayAgg:
        return ArrayAgg(
            'person__full_name',
            distinct=True,
            filter=Q(personfilmwork__role__exact=role),
        )

    def get_queryset(self):
        return (
            self.model.objects.prefetch_related(
                'genres',
                'person',
            )
            .values()
            .annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=self._aggregate_person(PersonFilmwork.RoleType.ACTOR.value),
                directors=self._aggregate_person(
                    PersonFilmwork.RoleType.DIRECTOR.value
                ),
                writers=self._aggregate_person(PersonFilmwork.RoleType.PRODUCER.value),
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
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by: int = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)['object']
