from http import HTTPStatus
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Connection
from dtos.movie import MovieDto
from exceptions.common import ItemAlreadyExistsException, ItemNotFoundException
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie
from requests.movie import CreateMovieRequest, UpdateMovieRequest
from services.movie import MovieService

movie_router: APIRouter = APIRouter()


@movie_router.post(
    "/movies",
    tags=["Movies"],
    response_model=MovieDto,
    status_code=HTTPStatus.CREATED
)
def create_movie(request: CreateMovieRequest = Body()) -> JSONResponse:
    try:
        with Connection as db:
            data: MovieDto = MovieDto(**request.dict())

            created: MovieDto = MovieService(db=db).create_movie(data=data)

            response = jsonable_encoder(created)

            return JSONResponse(content=response)
    except ItemAlreadyExistsException as ex:
        raise HTTPException(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail=ex.args[0]
        )
    except Exception:
        raise


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
    with Connection as db:
        response = MovieService(db=db).get_movies(category=category, year=year)

        return JSONResponse(
            content=jsonable_encoder(response)
        )


@movie_router.get("/movies/{id}", tags=["Movies"], response_model=MovieDto)
def get_movie(id: int = Path(ge=1)) -> JSONResponse:
    try:
        with Connection as db:
            movie: Movie = MovieService(db=db).get_movie(movie_id=id)

            response = jsonable_encoder(movie)

            return JSONResponse(content=response)
    except ItemNotFoundException as ex:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ex.args[0]
        )
    except Exception:
        raise


@movie_router.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int) -> None:
    try:
        with Connection as db:
            MovieService(db=db).delete_movie(id)
    except ItemNotFoundException as ex:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ex.args[0]
        )
    except Exception:
        raise


@movie_router.put("/movies/{id}", tags=["Movies"], response_model=MovieDto)
def update_movie(id: int, request: UpdateMovieRequest = Body()) -> JSONResponse:
    try:
        with Connection as db:
            data: MovieDto = MovieDto(**request.dict())

            updated: MovieDto = MovieService(
                db=db
            ).update_movie(movie_id=id, data=data)

            response = jsonable_encoder(updated)

            return JSONResponse(content=response)
    except ItemNotFoundException as ex:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ex.args[0]
        )
    except Exception:
        raise
