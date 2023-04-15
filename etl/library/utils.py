import logging
from datetime import datetime, timezone
from library.state import State
from library.extractor import PostgresExtractor
from typing import Iterator
from schemas.sources import SourceMovie
from library.constants import extract_method_by_modified_type, state_name_map, ExtractObject

logger = logging.getLogger(__name__)


def get_updated_movies(
        state: State,
        extractor: PostgresExtractor,
        extract_object: ExtractObject
) -> Iterator[list[SourceMovie]]:
    """Логика обновления индексов.
    """
    state_name = state_name_map.get(extract_object)
    last_modified = state.get_state(state_name)

    if extract_object == ExtractObject.MOVIES and last_modified is None:
        state.set_state(state_name, datetime.fromtimestamp(0, tz=timezone.utc).isoformat())
        last_modified = state.get_state(state_name)

    if last_modified is not None:
        logger.info(f"Check update {extract_object} after {last_modified}")
        extract_method = getattr(extractor, extract_method_by_modified_type[state_name])

        for data in extract_method(last_modified):
            yield data

            if datetime.fromisoformat(last_modified) < data[-1].modified:
                state.set_state(state_name, data[-1].modified.isoformat())

    state.set_state(state_name, state.get_state('start_time'))
