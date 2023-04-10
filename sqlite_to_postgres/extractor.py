import logging
import os
import sqlite3
from typing import Iterator

from local_typing import TABLES_TYPE

from sqlite_to_postgres.schemas import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

logger = logging.getLogger(__name__)


TABLE_MAP = {
    'film_work': FilmWork,
    'genre': Genre,
    'person': Person,
    'person_film_work': PersonFilmWork,
    'genre_film_work': GenreFilmWork,
}


class Cursor:
    def __init__(self, conn: sqlite3.Connection):
        self.connection = conn
        self.cursor = None

    def __enter__(self) -> sqlite3.Cursor:
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, *args, **kwargs) -> None:
        self.cursor.close()


class SQLiteExtractor:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection = None

    def __enter__(self) -> 'SQLiteExtractor':
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row

        except Exception as e:
            logger.error(f'Ошибка соединения с БД SQLite: {e}')

        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.connection.close()

    def _run_sql(self, sql: str) -> Iterator[list[sqlite3.Row]]:
        load_package_size = int(os.environ.get('LOAD_PACKAGE_SIZE', 10))
        with Cursor(self.connection) as cursor:
            if cursor is None:
                return []

            cursor.execute(sql)
            while True:
                data = cursor.fetchmany(load_package_size)
                if not data:
                    break

                yield data

    def _extract_data(self) -> Iterator[list[TABLES_TYPE]]:
        for table_name in ('film_work', 'genre', 'person', 'person_film_work', 'genre_film_work'):
            sql = f"SELECT * FROM {table_name};"
            for rows in self._run_sql(sql):
                yield [TABLE_MAP[table_name].load(row) for row in rows]

    def extract_movies(self) -> Iterator[list[TABLES_TYPE]]:
        for data in self._extract_data():
            yield data
