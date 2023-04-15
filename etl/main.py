import os
from redis import Redis
from dotenv import load_dotenv
from library.state import State, RedisStorage, JsonFileStorage
from library.extractor import PostgresExtractor
from datetime import datetime, timezone
import time
import logging
from library.constants import StateName, extract_method_by_modified_type, state_name_map, ExtractObject
from library.utils import get_updated_movies


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

    state = State(storage)

    while True:
        state.set_state('start_time', datetime.now(timezone.utc).isoformat())

        with PostgresExtractor(dsn) as postgres_extractor:
            extract_objects = (ExtractObject.MOVIES, ExtractObject.PEOPLE, ExtractObject.GENRES)
            for extract_object in extract_objects:
                for updated_movies in get_updated_movies(state, postgres_extractor, extract_object):
                    print(len(updated_movies))

        logger.info(f'Sleeping {sleep_time} sec...')
        time.sleep(sleep_time)
