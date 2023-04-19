from pydantic import (
    BaseSettings,
    PostgresDsn,
    Field,
)


class Settings(BaseSettings):
    DEBUG: bool = Field(False, env='DEBUG')
    PG_DSN: PostgresDsn = Field('postgres://user:pass@localhost:5432/foobar', env='PG_DSN')
    ES_HOST: str = Field('localhost', env='ES_HOST')
    ES_PORT: str = Field('9200', env='ES_PORT')
    ES_SSL: bool = Field(True, env='ES_SSL')
    ES_SCHEMA_PATH: str = Field('es_schema.json', env='ES_SCHEMA_PATH')
    USE_REDIS: bool = Field(True, env='USE_REDIS')
    REDIS_HOST: str = Field('localhost', env='REDIS_HOST')
    REDIS_PORT: int = Field('6379', env='REDIS_PORT')
    JSON_STORAGE_FILE: str = Field('storage.json', env='JSON_STORAGE_FILE')
    ETL_LOAD_PACKAGE_SIZE: int = Field('5000', env='ETL_LOAD_PACKAGE_SIZE')
    SLEEP_TIME: int = Field(300, env='SLEEP_TIME')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
print(settings.PG_DSN)