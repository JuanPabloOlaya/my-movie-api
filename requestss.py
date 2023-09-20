from pydantic import BaseModel, Field


class CreateMovieRequest(BaseModel):
    id: int
    title: str = Field(max_length=50)
    overview: str = Field(max_length=100)
    year: str = Field(pattern="^[0-9]{4}$")
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(max_length=30)


class UpdateMovieRequest(BaseModel):
    title: str = Field(max_length=50)
    overview: str = Field(max_length=100)
    year: str = Field(pattern="^[0-9]{4}$")
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(max_length=30)


class LoginRequest(BaseModel):
    email: str
    password: str
