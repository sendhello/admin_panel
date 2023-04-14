import logging

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import DictCursor

from .local_typing import TABLES_TYPE

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


class PostgresSaver:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None

    def __enter__(self) -> 'PostgresSaver':
        try:
            self.connection = psycopg2.connect(**self.dsn, cursor_factory=DictCursor)
            self.connection.autocommit = True

        except Exception as e:
            logger.error(f'Ошибка соединения с БД Postgres: {e}')

        return self

    def __exit__(self, *args, **kwargs) -> None:
        if self.connection is None:
            return None

        self.connection.close()

    def _run_sql(self, table_data: list[TABLES_TYPE]):
        if not table_data:
            return None

        table_fields = tuple(table_data[0].__dict__)
        data = tuple(tuple(map(lambda x: getattr(row, x), table_fields)) for row in table_data)
        with Cursor(self.connection) as cursor:
            if cursor is None:
                return None

            mogrify_format = f"({', '.join(['%s']*len(table_fields))})"
            values = ','.join(cursor.mogrify(mogrify_format, item).decode() for item in data)
            try:
                cursor.execute(f"""
                    INSERT INTO content.{table_data[0].__name__} ({', '.join(table_fields)})
                    VALUES {values}
                    ON CONFLICT (id) DO NOTHING;
                """)

            except Exception as e:
                logger.error(f'Ошибка выполнения запроса в БД Postgres: {e}')
                return []

    def save_all_data(self, data: list[TABLES_TYPE]):
        self._run_sql(data)
