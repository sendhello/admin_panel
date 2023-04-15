from enum import Enum


class StateName(str, Enum):
    """Переменные состояния.
    """
    START_TIME = 'start_time'
    FILM_WORK_LAST_MODIFIED = 'film_work_last_modified'
    PERSON_LAST_MODIFIED = 'person_last_modified'
    GENRE_LAST_MODIFIED = 'genre_last_modified'


class ExtractObject(str, Enum):
    MOVIES = 'movies'
    PEOPLE = 'people'
    GENRES = 'genres'


state_name_map = {
    ExtractObject.MOVIES: StateName.FILM_WORK_LAST_MODIFIED,
    ExtractObject.PEOPLE: StateName.PERSON_LAST_MODIFIED,
    ExtractObject.GENRES: StateName.GENRE_LAST_MODIFIED,
}

extract_method_by_modified_type = {
    StateName.FILM_WORK_LAST_MODIFIED: 'extract_updated_movies',
    StateName.PERSON_LAST_MODIFIED: 'extract_updated_people',
    StateName.GENRE_LAST_MODIFIED: 'extract_updated_genres',
}
