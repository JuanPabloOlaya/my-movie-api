from http import HTTPStatus
import json
from typing import Any, Tuple
from fastapi import Body, Depends, FastAPI, Path, Query
from sqlalchemy import Select, select
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
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

Base.metadata.create_all(bind=engine)

movies: list[MovieDto] = [
    MovieDto(
        id=1,
        title='Avatar',
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year='2009',
        rating=7.8,
        category='Acción'
    ),
    MovieDto(
        id=2,
        title='Avatar 2',
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year='2022',
        rating=10.0,
        category='Ciencia Ficción'
    )
]


@app.get("/", tags=["Home"], response_class=HTMLResponse)
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


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

    with Session() as db:
        statement: Select[Tuple] = select(MovieModel).filter_by(**filters)

        response = db.scalars(statement).all()

        return JSONResponse(
            content=jsonable_encoder(response)
        )


@app.get("/movies/{id}", tags=["Movies"], response_model=MovieDto)
def get_movie(id: int = Path(ge=1)) -> JSONResponse:
    with Session() as db:
        movie: MovieModel = db.get(MovieModel, id)

        if (not movie):
            raise ItemNotFoundException(
                f"Movie with id <{id}> does not exists"
            )

        response = jsonable_encoder(movie)

        return JSONResponse(content=response)


@app.post(
    "/movies",
    tags=["Movies"],
    response_model=MovieDto,
    status_code=HTTPStatus.CREATED
)
def create_movie(request: CreateMovieRequest = Body()) -> JSONResponse:
    db = Session()

    movie: MovieModel = MovieModel(
        **request.model_dump()
    )

    db.add(movie)
    db.commit()

    response = jsonable_encoder(movie)

    return JSONResponse(content=response)


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> None:
    movie: MovieDto = None

    for m in movies:
        if (m.id == id):
            movie = m

            break

    if (not movie):
        raise ItemNotFoundException(
            detail=f"Movie with ID <{id}> was not found"
        )

    movies.remove(movie)


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, request: UpdateMovieRequest = Body()) -> JSONResponse:
    movieIndex: int = None

    for index, m in enumerate(movies):
        if (m.id == id):
            movieIndex = index

            break

    if movieIndex is None:
        raise ItemNotFoundException(
            detail=f"Movie with ID <{id}> was not found"
        )

    movies[movieIndex] = MovieDto(
        id=id,
        title=request.title,
        overview=request.overview,
        year=request.year,
        rating=request.rating,
        category=request.category
    )

    response = jsonable_encoder(movies[movieIndex])

    return JSONResponse(content=response)
