from pydantic import BaseModel


class MovieDto(BaseModel):
    id: int
    title: str
    overview: str
    year: str
    rating: float
    category: str
