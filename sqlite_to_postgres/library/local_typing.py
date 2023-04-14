from typing import Union

from .schemas import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

TABLES_TYPE = Union[FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork]
