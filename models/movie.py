from sqlmodel import Field, SQLModel


class Movie(SQLModel, table=True):
    __tablename__: str = "movies"

    id: int = Field(default=None, primary_key=True)
    title: str
    overview: str
    year: int
    rating: float
    category: str
