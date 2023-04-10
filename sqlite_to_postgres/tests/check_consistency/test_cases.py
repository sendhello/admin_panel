import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()


SQLITE_PATH = os.environ.get('SQLITE_DB')
DSN = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
}
TABLES = (
    'film_work',
    'genre',
    'person',
    'genre_film_work',
    'person_film_work',
)


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn

    conn.close()


def test_compare_databases():
    with (
        conn_context(SQLITE_PATH) as sqlite_conn,
        psycopg2.connect(**DSN, cursor_factory=DictCursor) as postgres_conn,
        postgres_conn.cursor() as postgres_cursor
    ):
        sqlite_cursor = sqlite_conn.cursor()

        for table_name in TABLES:
            sqlite_cursor.execute(f"SELECT * FROM {table_name};")
            sqlite_results = sqlite_cursor.fetchall()

            postgres_cursor.execute(f"SELECT * FROM content.{table_name}")
            postgres_results = postgres_cursor.fetchall()

            # Сравнение размеров таблиц
            assert len(sqlite_results) == len(postgres_results)

            postgres_data = {res['id']: res for res in postgres_results}
            for row in sqlite_results:
                # Проверка наличия ID записи sqlite в postgres
                assert row['id'] in postgres_data

                # Поля created и modified в БД-источнике называются по-другому,
                # поэтому сначала сравниваем сами поля, а потом остатки данных без этих полей
                row_data = dict(row)
                postgres_row_data = dict(postgres_data[row['id']])
                if row_data.get('created_at') and postgres_row_data.get('created'):
                    assert datetime.fromisoformat(row_data.get('created_at')) == postgres_row_data.get('created')
                row_data.pop('created_at', None)
                postgres_row_data.pop('created', None)

                if row_data.get('updated_at') and postgres_row_data.get('modified'):
                    assert datetime.fromisoformat(row_data.get('updated_at')) == postgres_row_data.get('modified')
                row_data.pop('updated_at', None)
                postgres_row_data.pop('modified', None)

                # Также в БД-источнике отсутствуют некоторые поля, не сравниваем их
                postgres_row_data.pop('certificate', None)
                postgres_row_data.pop('gender', None)

                # Проверка записей (без полей created и modified)
                assert row_data == postgres_row_data
