from http import HTTPStatus
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import select
from config.database import Connection
from dtos.movie import MovieDto
from exceptions.common import ItemAlreadyExistsException, ItemNotFoundException
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie
from requests.movie import CreateMovieRequest, UpdateMovieRequest

movie_router = APIRouter()


@movie_router.post(
    "/movies",
    tags=["Movies"],
    response_model=MovieDto,
    status_code=HTTPStatus.CREATED
)
def create_movie(request: CreateMovieRequest = Body()) -> JSONResponse:
    with Connection as db:
        movie: Movie = db.get(Movie, request.id)

        if (movie):
            raise ItemAlreadyExistsException(
                f"The movie with id <{request.id}> already exists"
            )

        movie: Movie = Movie(
            **request.dict()
        )

        db.add(movie)
        db.commit()

        response = jsonable_encoder(request)

        return JSONResponse(content=response)


@movie_router.get(
    "/movies",
    tags=["Movies"],
    response_model=list[MovieDto],
    dependencies=[Depends(JWTBearer())]
)
def get_movies(
    category: str = Query(
        default=None,
        max_length=30
    ),
    year: int = Query(
        default=None,
        le=9999,
        ge=1000
    )
) -> JSONResponse:
    filters: dict = {}

    if (category):
        filters["category"] = category

    if (year):
        filters["year"] = year

    with Connection as db:
        statement = select(Movie).filter_by(**filters)

        response = db.exec(statement).all()

        return JSONResponse(
            content=jsonable_encoder(response)
        )


@movie_router.get("/movies/{id}", tags=["Movies"], response_model=MovieDto)
def get_movie(id: int = Path(ge=1)) -> JSONResponse:
    with Connection as db:
        movie: Movie = db.get(Movie, id)

        if (not movie):
            raise ItemNotFoundException(
                f"Movie with id <{id}> does not exists"
            )

        response = jsonable_encoder(movie)

        return JSONResponse(content=response)


@movie_router.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> None:
    with Connection as db:
        movie: Movie = db.get(Movie, id)

        if not movie:
            raise ItemNotFoundException(
                f"The movie with ID <{id}> does not exists"
            )

        db.delete(movie)

        db.commit()


@movie_router.put("/movies/{id}", tags=["Movies"], response_model=MovieDto)
def update_movie(id: int, request: UpdateMovieRequest = Body()) -> JSONResponse:
    with Connection as db:
        movie: Movie = db.get(Movie, id)

        if not movie:
            raise ItemNotFoundException(
                f"The movie with ID <{id}> does not exists"
            )

        movie.category = request.category
        movie.overview = request.overview
        movie.rating = request.rating
        movie.title = request.title
        movie.year = request.year

        db.add(movie)
        db.commit()
        db.refresh(movie)

        response = jsonable_encoder(movie)

        return JSONResponse(content=response)
