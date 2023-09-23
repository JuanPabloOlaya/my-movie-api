from http import HTTPStatus
import json
from typing import Any, Tuple
from fastapi import Body, Depends, FastAPI, Path, Query
from sqlmodel import select
from models.movie import Movie as MovieModel
from config.database import create_db_and_tables, Connection
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from exceptions import ItemAlreadyExistsException, ItemNotFoundException, LoginException
from jwt_manager import create_token
from middlewares import JWTBearer

from dtos import MovieDto
from requestss import CreateMovieRequest, LoginRequest, UpdateMovieRequest

app: FastAPI = FastAPI()

app.title = "My Movie API"
app.version = "0.0.1"

create_db_and_tables()


@app.get("/", tags=["Home"], response_class=HTMLResponse)
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


@app.post(
    "/movies",
    tags=["Movies"],
    response_model=MovieDto,
    status_code=HTTPStatus.CREATED
)
def create_movie(request: CreateMovieRequest = Body()) -> JSONResponse:
    with Connection as db:
        movie: MovieModel = MovieModel(
            **request.dict()
        )

        db.add(movie)
        db.commit()

        response = jsonable_encoder(request)

        return JSONResponse(content=response)


@app.post("/login", tags=["Auth"])
def login(request: LoginRequest) -> Any:
    if (request.email == "mail@mail.com" and request.password == "123456"):
        token: str = create_token(request.__dict__)

        return JSONResponse(status_code=200, content=token)

    raise LoginException()


@app.get(
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
        statement = select(MovieModel).filter_by(**filters)

        response = db.exec(statement).all()

        return JSONResponse(
            content=jsonable_encoder(response)
        )


@app.get("/movies/{id}", tags=["Movies"], response_model=MovieDto)
def get_movie(id: int = Path(ge=1)) -> JSONResponse:
    with Connection as db:
        movie: MovieModel = db.get(MovieModel, id)

        if (not movie):
            raise ItemNotFoundException(
                f"Movie with id <{id}> does not exists"
            )

        response = jsonable_encoder(movie)

        return JSONResponse(content=response)


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> None:
    with Connection as db:
        movie: MovieModel = db.get(MovieModel, id)

        if not movie:
            raise ItemNotFoundException(
                f"The movie with ID <{id}> does not exists"
            )

        db.delete(movie)

        db.commit()


@app.put("/movies/{id}", tags=["Movies"], response_model=MovieDto)
def update_movie(id: int, request: UpdateMovieRequest = Body()) -> JSONResponse:
    with Connection as db:
        movie: MovieModel = db.get(MovieModel, id)

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
