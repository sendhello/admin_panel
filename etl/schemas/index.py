from pydantic import BaseModel, Field
from uuid import UUID


class IndexData(BaseModel):
    index: str = Field(alias='_index')
    id: str = Field(alias='_id')


class Index(BaseModel):
    index: IndexData
