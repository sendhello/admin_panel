import json
import os
from utils import backoff
import requests
from schemas.models import Movie
from schemas.index import Index, IndexData


class ElasticsearchLoader:
    def __init__(self, host: str, port: str, ssl: bool):
        protocol = 'https' if ssl else 'http'
        self.url = f'{protocol}://{host}:{port}'

    @backoff()
    def _get(self, path: str):
        return requests.get(f'{self.url}/{path}')

    @backoff()
    def _put(self, path: str, data: dict = None):
        headers = {'Content-type': 'application/json'}
        return requests.put(f'{self.url}/{path}', data=json.dumps(data), headers=headers)

    @backoff()
    def _post(self, path: str, data: dict | str = None, json=None):
        headers = {'Content-type': 'application/x-ndjson'}
        return requests.post(f'{self.url}/{path}', data=data, json=json, headers=headers)

    @staticmethod
    def _create_bulk(model: Movie, schema: str):
        """Генерация x-ndjson пары строк для отправки bulk запроса в Elasticsearch.
        """
        index = Index(
            index=IndexData(
                _id=model.id,
                _index=schema,
            )
        )
        return f"{index.json(by_alias=True)}\n{model.json()}\n"

    def create_index(self, schema: dict):
        check_schema_res = self._get('movies')
        if check_schema_res.status_code == 404:
            res = self._put('movies', schema)
            if res.json().get('error'):
                raise RuntimeError('Failed to create index schema')

    def load_movies(self, movies: list[Movie]):
        data = ''.join(self._create_bulk(movie, 'movies') for movie in movies)
        res = self._post('_bulk', data=data)
