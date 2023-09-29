from http import HTTPStatus
from typing import Self


class ItemNotFoundException(Exception):
    pass


class ItemAlreadyExistsException(Exception):
    pass
