import abc
from typing import Any
import json
from redis import Redis


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        with open(self.file_path, 'w') as f:
            json.dump(state, f)

    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""
        try:
            with open(self.file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


class RedisStorage(BaseStorage):
    """Реализация хранилища, использующего Redis."""

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище.
        """
        self._redis.set('data', json.dumps(state))

    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""
        data = self._redis.get('data')
        if data is None:
            return {}

        return json.loads(self._redis.get('data'))


class State:
    """Класс для работы с состояниями.
    """
    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа.
        """
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str, default=None) -> Any:
        """Получить состояние по определённому ключу.
        """
        state = self.storage.retrieve_state()
        res = state.get(key)
        if res is None:
            return default

        return res
