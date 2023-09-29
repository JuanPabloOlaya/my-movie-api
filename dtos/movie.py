from typing import Optional
from pydantic import BaseModel


class MovieDto(BaseModel):
    id: Optional[int]
    title: str
    overview: str
    year: str
    rating: float
    category: str
