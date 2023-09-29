from typing import Any
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from exceptions.auth import LoginException
from requests.auth import LoginRequest

from utils.jwt_manager import create_token


auth_router = APIRouter()


@auth_router.post("/login", tags=["Auth"])
def login(request: LoginRequest) -> Any:
    if (request.email == "mail@mail.com" and request.password == "123456"):
        token: str = create_token(request.__dict__)

        return JSONResponse(status_code=200, content=token)

    raise LoginException()
