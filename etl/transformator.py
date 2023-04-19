from schemas import Movie, Person, RoleType, SourceMovie


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
                person_id = str(source_movie.person_id)
                full_name = source_movie.full_name
                if person_id not in {actor.id for actor in movies[movie_id].actors}:
                    movies[movie_id].actors_names.append(full_name)
                    movies[movie_id].actors.append(Person(
                        id=person_id,
                        name=full_name,
                    ))

            elif source_movie.role == RoleType.WRITER:
                person_id = str(source_movie.person_id)
                full_name = source_movie.full_name
                if person_id not in {writer.id for writer in movies[movie_id].writers}:
                    movies[movie_id].writers_names.append(full_name)
                    movies[movie_id].writers.append(Person(
                        id=person_id,
                        name=full_name,
                    ))

        return list(movies.values())
