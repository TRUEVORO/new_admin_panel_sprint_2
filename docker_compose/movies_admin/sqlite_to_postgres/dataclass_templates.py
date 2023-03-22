import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class _TimeStampedMixin:
    created: datetime.date
    modified: datetime.date


@dataclass(frozen=True)
class FilmWork(_TimeStampedMixin):
    title: str
    description: str
    creation_date: str
    rating: float = field(default=0.0)
    type: str = field(default='movie')
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre(_TimeStampedMixin):
    name: str
    description: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person(_TimeStampedMixin):
    full_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreFilmWork:
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created: datetime.date
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonFilmWork:
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created: datetime.date
    id: uuid.UUID = field(default_factory=uuid.uuid4)


movies_mapper = {
    'film_work': FilmWork,
    'genre': Genre,
    'person': Person,
    'genre_film_work': GenreFilmWork,
    'person_film_work': PersonFilmWork,
}
