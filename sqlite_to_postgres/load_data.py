import os

from dotenv import load_dotenv
from extractor import SQLiteExtractor
from saver import PostgresSaver

load_dotenv()


if __name__ == '__main__':
    sqlite_path = os.environ.get('SQLITE_DB')
    dsn = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
    }

    with SQLiteExtractor(sqlite_path) as sqlite_extractor, PostgresSaver(dsn) as postgres_saver:
        for data in sqlite_extractor.extract_movies():
            postgres_saver.save_all_data(data)
