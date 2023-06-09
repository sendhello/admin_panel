from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MoviesType(str, Enum):
    """Типы фильмов.
    """
    MOVIE = 'movie'
    TV_SHOW = 'tv_show'


class RoleType(str, Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'


class SourceId(BaseModel):
    """Модель выгрузки IDs из БД.
    """
    id: UUID
    modified: datetime


class SourceMovie(BaseModel):
    """Модель фильма-персона-жанр выгрузки из БД.
    """
    id: UUID
    title: str
    description: str | None
    rating: float | None
    type: MoviesType
    created: datetime
    modified: datetime
    role: RoleType | None
    person_id: UUID | None
    full_name: str | None
    genre_name: str | None
