from fastapi.security import HTTPBearer
from starlette.requests import Request
from exceptions import UnauthorizedException

from jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth_data = await super().__call__(request)
        data = validate_token(auth_data.credentials)

        if (data["email"] != "mail@mail.com"):
            raise UnauthorizedException()
