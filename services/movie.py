from typing import List, Self
from sqlmodel import Session, select
from dtos.movie import MovieDto
from exceptions.common import ItemAlreadyExistsException, ItemNotFoundException

from models.movie import Movie


class MovieService():
    def __init__(self: Self, db: Session) -> None:
        self.db = db

    def get_movies(self: Self, category: str = None, year: str = None) -> List[Movie]:
        filters: dict = {}

        if (category):
            filters["category"] = category

        if (year):
            filters["year"] = year

        statement = select(Movie).filter_by(**filters)

        return self.db.exec(statement).all()

    def get_movie(self: Self, movie_id: int) -> Movie:
        movie: Movie = self.db.get(Movie, movie_id)

        if (not movie):
            raise ItemNotFoundException(
                f"Movie with id <{movie_id}> does not exists"
            )

        return movie

    def create_movie(self: Self, data: MovieDto) -> MovieDto:
        movie: Movie = self.db.get(Movie, data.id)

        if (movie):
            raise ItemAlreadyExistsException(
                f"The movie with id <{data.id}> already exists"
            )

        movie: Movie = Movie(
            **data.dict()
        )

        self.db.add(movie)
        self.db.commit()

        return data

    def delete_movie(self: Self, movie_id: int) -> None:
        movie: Movie = self.db.get(Movie, movie_id)

        if (not movie):
            raise ItemNotFoundException(
                f"The movie with id <{movie_id}> does not exists"
            )

        self.db.delete(movie)
        self.db.commit()

    def update_movie(self: Self, movie_id: int, data: MovieDto) -> MovieDto:
        movie: Movie = self.db.get(Movie, movie_id)

        if not movie:
            raise ItemNotFoundException(
                f"The movie with ID <{movie_id}> does not exists"
            )

        movie.category = data.category
        movie.overview = data.overview
        movie.rating = data.rating
        movie.title = data.title
        movie.year = data.year

        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)

        return MovieDto(**movie.dict())
