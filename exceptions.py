from http import HTTPStatus
from typing import Any, Dict, Optional, Self
from fastapi import HTTPException
from pydantic import BaseModel


class ItemNotFoundException(HTTPException):
    def __init__(self: Self, detail: str) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)


class ItemAlreadyExistsException(HTTPException):
    def __init__(self: Self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.PRECONDITION_FAILED,
            detail=detail
        )
