from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class MoviesType(str, Enum):
    """Типы фильмов.
    """
    MOVIE = 'movie'
    TV_SHOW = 'tv_show'


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
    role: str | None
    person_id: UUID | None
    full_name: str | None
    genre_name: str | None
