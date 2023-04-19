import json
import logging
import time
from datetime import datetime, timezone

from redis import Redis

from extractor import PostgresExtractor
from loader import ElasticsearchLoader
from settings import settings
from state import JsonFileStorage, RedisStorage, State
from transformator import Transformator

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    if settings.USE_REDIS:
        redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        storage = RedisStorage(redis)
    else:
        storage = JsonFileStorage(settings.JSON_STORAGE_FILE)

    with open(settings.ES_SCHEMA_PATH) as f:
        es_schema = json.load(f)

    state = State(storage)
    loader = ElasticsearchLoader(host=settings.ES_HOST, port=settings.ES_PORT, ssl=settings.ES_SSL)
    loader.create_index(schema=es_schema)

    while True:
        state.set_state('start_time', datetime.now(timezone.utc).isoformat())

        with PostgresExtractor(settings.PG_DSN) as postgres_extractor:
            for source_movies in postgres_extractor.get_updated_movies(state):
                transformator = Transformator(source_movies)
                movies = transformator.get_movies()
                loader.load_movies(movies)

        logger.info(f'Sleeping {settings.SLEEP_TIME} sec...')
        time.sleep(settings.SLEEP_TIME)
