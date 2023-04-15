import logging
import os
from typing import Any, Iterator

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor

from library.sql import FILM_WORK_BY_IDS_SQL, FILM_WORK_BY_LAST_MODIFIED_SQL, PERSON_BY_LAST_MODIFIED_SQL, \
    GENRE_BY_LAST_MODIFIED_SQL, FILM_WORK_IDS_BY_PERSON_IDS_SQL, FILM_WORK_IDS_BY_GENRE_IDS_SQL
from schemas.sources import SourceMovie, SourceId

logger = logging.getLogger(__name__)


class Cursor:
    def __init__(self, conn: _connection):
        self.connection = conn
        self.cursor = None

    def __enter__(self) -> _cursor:
        if self.connection:
            self.cursor = self.connection.cursor()

        return self.cursor

    def __exit__(self, *args, **kwargs) -> None:
        if self.cursor is None:
            return None

        self.cursor.close()


class PostgresExtractor:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None

    def __enter__(self) -> 'PostgresExtractor':
        try:
            self.connection = psycopg2.connect(**self.dsn, cursor_factory=DictCursor)
            self.connection.autocommit = True

        except Exception as e:
            logger.error(f'Connection error with Postgres DB: {e}')

        return self

    def __exit__(self, *args, **kwargs) -> None:
        if self.connection is None:
            return None

        self.connection.close()

    def _run_sql(self, sql: str) -> Iterator[list[Any]]:
        load_package_size = int(os.getenv('LOAD_PACKAGE_SIZE', 10))
        with Cursor(self.connection) as cursor:
            if cursor is None:
                return []

            try:
                cursor.execute(sql)
                while True:
                    data = cursor.fetchmany(load_package_size)
                    if not data:
                        break

                    yield data

            except Exception as e:
                logger.error(f'Error of SQL request: {e}')
                return []

    def _get_updated_records(self, sql: str, last_modified: str) -> Iterator[list[SourceId]]:
        """Получаем список IDs обновленных записей.
        """
        for rows in self._run_sql(sql.format(last_modified=last_modified)):
            yield [SourceId.parse_obj(row) for row in rows]

    def _get_film_work_ids(self, sql: str, raw_record_ids: list[SourceId]) -> Iterator[list[SourceId]]:
        """Получаем список IDs фильмов, в которых есть обновленные жанры или люди.
        """
        record_ids = '(' + ', '.join(f'\'{raw_id.id}\'' for raw_id in raw_record_ids) + ')'
        for rows in self._run_sql(sql.format(record_ids=record_ids)):
            yield [SourceId.parse_obj(row) for row in rows]

    def _get_film_work_with_ids(self, raw_film_work_ids: list[SourceId]) -> Iterator[list[SourceId]]:
        """Получаем фильмы, по IDs.
        """
        film_work_ids = '(' + ', '.join(f'\'{id_raw.id}\'' for id_raw in raw_film_work_ids) + ')'
        for rows in self._run_sql(FILM_WORK_BY_IDS_SQL.format(film_work_ids=film_work_ids)):
            yield [SourceMovie.parse_obj(row) for row in rows]

    def extract_updated_movies(self, last_modified: str) -> Iterator[list[SourceMovie]]:
        """Получаем фильмы, обновленные позже last_modified.
        """
        for rows in self._run_sql(FILM_WORK_BY_LAST_MODIFIED_SQL.format(last_modified=last_modified)):
            yield [SourceMovie.parse_obj(row) for row in rows]

    def extract_updated_people(self, last_modified: str) -> Iterator[list[SourceMovie]]:
        """Получаем фильмы, в которых участвовали обновленные персоны.
        """
        for people in self._get_updated_records(PERSON_BY_LAST_MODIFIED_SQL, last_modified):
            for film_work_ids in self._get_film_work_ids(FILM_WORK_IDS_BY_PERSON_IDS_SQL, people):
                for film_works in self._get_film_work_with_ids(film_work_ids):
                    yield film_works

    def extract_updated_genres(self, last_modified: str) -> Iterator[list[SourceMovie]]:
        """Получаем фильмы, в которых обновили жанр.
        """
        for people in self._get_updated_records(GENRE_BY_LAST_MODIFIED_SQL, last_modified):
            for film_work_ids in self._get_film_work_ids(FILM_WORK_IDS_BY_GENRE_IDS_SQL, people):
                for film_work in self._get_film_work_with_ids(film_work_ids):
                    yield film_work
