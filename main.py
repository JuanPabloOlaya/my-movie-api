from fastapi import FastAPI
from middlewares.error_handler import ErrorHandler
from config.database import create_db_and_tables
from fastapi.responses import HTMLResponse
from routers.movie import movie_router
from routers.auth import auth_router

app: FastAPI = FastAPI()

app.title = "My Movie API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(auth_router)

create_db_and_tables()


@app.get("/", tags=["Home"], response_class=HTMLResponse)
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")
