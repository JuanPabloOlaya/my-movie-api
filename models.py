from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: str
    rating: float
    category: str
