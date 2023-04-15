from schemas.sources import SourceMovie
from pydantic import BaseModel, Field
from uuid import UUID
from schemas.sources import RoleType
from typing import Dict
from schemas.models import Movie, Person


class Transformator:
    def __init__(self, source_movies: list[SourceMovie]):
        self.source_movies = source_movies

    def get_movies(self) -> list[Movie]:
        movies = {}
        for source_movie in self.source_movies:
            movie_id = source_movie.id

            if movie_id not in movies:
                movies[movie_id] = Movie(
                    id=str(movie_id),
                    imdb_rating=source_movie.rating,
                    genre=source_movie.genre_name,
                    title=source_movie.title,
                    description=source_movie.description,
                )

            if source_movie.role == RoleType.DIRECTOR:
                movies[movie_id].director = source_movie.full_name

            elif source_movie.role == RoleType.ACTOR:
                movies[movie_id].actors_names.append(source_movie.full_name)
                movies[movie_id].actors.append(Person(
                    id=str(source_movie.person_id),
                    name=source_movie.full_name,
                ))

            elif source_movie.role == RoleType.WRITER:
                movies[movie_id].writers_names.append(source_movie.full_name)
                movies[movie_id].writers.append(Person(
                    id=str(source_movie.person_id),
                    name=source_movie.full_name,
                ))

        return list(movies.values())
