import os
from redis import Redis
from dotenv import load_dotenv
from state import State, RedisStorage, JsonFileStorage
from extractor import PostgresExtractor
from datetime import datetime, timezone
import time
import json
import logging
from loader import ElasticsearchLoader
from constants import StateName, extract_method_by_modified_type, state_name_map, ExtractObject
from transformator import Transformator


load_dotenv()
debug = os.getenv('DEBUG', 'False') in ('True', 'true')
logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    dsn = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': os.getenv('DB_PORT', 5432),
    }

    es_host = os.getenv('ES_HOST', '127.0.0.1')
    es_port = os.getenv('ES_PORT', '9200')
    es_ssl = os.getenv('ES_SSL', 'True') in ('True', 'true')
    es_schema_path =os.getenv('ES_SCHEMA', 'es_schema.json')

    use_redis = os.getenv('USE_REDIS', 'False') in ('True', 'true')
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    json_storage_file = os.getenv('JSON_STORAGE_FILE', 'storage.json')
    sleep_time = int(os.getenv('SLEEP_TIME', '600'))

    if use_redis:
        redis = Redis(host=redis_host, port=redis_port)
        storage = RedisStorage(redis)
    else:
        storage = JsonFileStorage(json_storage_file)

    with open(es_schema_path) as f:
        es_schema = json.load(f)

    state = State(storage)
    loader = ElasticsearchLoader(host=es_host, port=es_port, ssl=es_ssl)
    loader.create_index(schema=es_schema)

    while True:
        state.set_state('start_time', datetime.now(timezone.utc).isoformat())

        with PostgresExtractor(dsn) as postgres_extractor:
            for source_movies in postgres_extractor.get_updated_movies(state):
                transformator = Transformator(source_movies)
                movies = transformator.get_movies()
                loader.load_movies(movies)

        logger.info(f'Sleeping {sleep_time} sec...')
        time.sleep(sleep_time)
