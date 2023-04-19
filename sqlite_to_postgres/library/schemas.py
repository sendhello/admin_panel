import sqlite3
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from uuid import UUID


class FilmWorkType(str, Enum):
    MOVIE = 'movie'
    TV_SHOW = 'tv_show'


class RoleType(str, Enum):
    ACTOR = 'actor'
    PRODUCER = 'producer'
    DIRECTOR = 'director'


@dataclass
class BaseMinimalModel:
    """Базовая минимальная схема.
    """
    id: UUID
    created: datetime

    @classmethod
    def load(cls, row: sqlite3.Row) -> 'BaseMinimalModel':
        data = dict(row)
        created = data.pop('created_at')
        return cls(
            created=created,
            **data
        )


@dataclass
class BaseModel(BaseMinimalModel):
    """Базовая схема.
    """
    modified: datetime

    @classmethod
    def load(cls, row: sqlite3.Row) -> 'BaseModel':
        data = dict(row)
        created = data.pop('created_at')
        modified = data.pop('updated_at')
        return cls(
            created=created,
            modified=modified,
            **data,
        )


@dataclass
class FilmWork(BaseModel):
    """Схема Фильма.
    """
    title: str
    description: str
    creation_date: date
    rating: float
    type: FilmWorkType
    file_path: str

    __name__ = 'film_work'


@dataclass
class Genre(BaseModel):
    """Схема жанра.
    """
    name: str
    description: str

    __name__ = 'genre'


@dataclass
class Person(BaseModel):
    """Схема персоны.
    """
    full_name: str

    __name__ = 'person'


@dataclass
class GenreFilmWork(BaseMinimalModel):
    """Схема связей жанров и фильмов.
    """
    film_work_id: str
    genre_id: str

    __name__ = 'genre_film_work'


@dataclass
class PersonFilmWork(BaseMinimalModel):
    """Схема связей персон и фильмов.
    """
    film_work_id: str
    person_id: str
    role: RoleType

    __name__ = 'person_film_work'
