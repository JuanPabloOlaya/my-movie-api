from http import HTTPStatus
from typing import Self
from fastapi import HTTPException


class ItemNotFoundException(HTTPException):
    def __init__(self: Self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail=detail
        )


class ItemAlreadyExistsException(HTTPException):
    def __init__(self: Self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail=detail
        )
