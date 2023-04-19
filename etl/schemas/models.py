from pydantic import BaseModel, Field


class Person(BaseModel):
    """Модель персоны для индекса.
    """
    id: str
    name: str


class Movie(BaseModel):
    """Модель индекса.
    """
    id: str
    imdb_rating: float | None
    genre: str | None
    title: str
    description: str | None
    director: str = Field(default_factory=str)
    actors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)
    actors: list[Person] = Field(default_factory=list)
    writers: list[Person] = Field(default_factory=list)
