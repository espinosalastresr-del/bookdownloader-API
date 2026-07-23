from pydantic import BaseModel, Field, HttpUrl


class Book(BaseModel):
    id: str = Field(..., description="Identificador del libro")
    md5: str

    title: str
    author: str | None = None
    publisher: str | None = None

    year: str | None = None
    language: str | None = None

    file_type: str | None = None
    size: str | None = None

    cover: HttpUrl | None = None


class SearchResponse(BaseModel):
    total: int
    books: list[Book]


class HealthResponse(BaseModel):
    status: str
    version: str