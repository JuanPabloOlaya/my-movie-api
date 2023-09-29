from http import HTTPStatus
from typing import Self
from fastapi import HTTPException


class LoginException(HTTPException):
    def __init__(self: Self) -> None:
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid login credentials"
        )


class UnauthorizedException(HTTPException):
    def __init__(self: Self) -> None:
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid credentials"
        )
