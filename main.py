from http import HTTPStatus
import json
from fastapi import Body, FastAPI, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from exceptions import ItemAlreadyExistsException, ItemNotFoundException

from models import Movie
from requestss import CreateMovieRequest, UpdateMovieRequest

app: FastAPI = FastAPI()

app.title = "My Movie API"
app.version = "0.0.1"

movies: list[Movie] = [
    Movie(
        id=1,
        title='Avatar',
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year='2009',
        rating=7.8,
        category='Acción'
    ),
    Movie(
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


@app.get("/movies", tags=["Movies"], response_model=list[Movie])
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
    if (not category and not year):

        return JSONResponse(content=jsonable_encoder(movies))

    response: list[Movie] = []

    if (not category and year):
        response = list(
            filter(
                lambda movie: movie.year == year, movies
            )
        )

        return JSONResponse(
            content=jsonable_encoder(response)
        )

    if (not year and category):
        response = list(
            filter(
                lambda movie: movie.category == category,
                movies
            )
        )

        return JSONResponse(
            content=jsonable_encoder(response)
        )

    response = list(
        filter(
            lambda movie: movie.category == category and movie.year == str(
                year),
            movies
        )
    )

    return JSONResponse(
        content=jsonable_encoder(response)
    )


@app.get("/movies/{id}", tags=["Movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> JSONResponse:
    movie: Movie = None
    iterator: int = 0

    while not movie and iterator < len(movies):
        current_movie: Movie = movies[iterator]

        if (current_movie.id == id):
            movie = current_movie

        iterator += 1

    if (not movie):
        raise ItemNotFoundException(
            detail=f"Movie with ID <{id}> does not exists"
        )

    response = jsonable_encoder(movie)

    return JSONResponse(content=response)


@app.post(
    "/movies",
    tags=["Movies"],
    response_model=Movie,
    status_code=HTTPStatus.CREATED
)
def create_movie(request: CreateMovieRequest = Body()) -> JSONResponse:
    coincidences: list[Movie] = list(
        filter(lambda movie: movie.id == request.id, movies))

    if (len(coincidences)):
        raise ItemAlreadyExistsException(
            detail=f"Movie with ID <{id}> already exists"
        )

    movie: Movie = Movie(
        id=request.id,
        title=request.title,
        overview=request.overview,
        year=request.year,
        rating=request.rating,
        category=request.category
    )

    movies.append(movie)

    response = jsonable_encoder(movie)

    return JSONResponse(content=response)


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> None:
    movie: Movie = None

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

    movies[movieIndex] = Movie(
        id=id,
        title=request.title,
        overview=request.overview,
        year=request.year,
        rating=request.rating,
        category=request.category
    )

    response = jsonable_encoder(movies[movieIndex])

    return JSONResponse(content=response)
