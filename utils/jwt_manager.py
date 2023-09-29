from typing import Any
from jwt import decode, encode


def create_token(data: dict[str, Any]) -> str:
    return encode(
        payload=data,
        key="my_secret_key",
        algorithm="HS256"
    )


def validate_token(token: str) -> dict[str, Any]:
    return decode(token, key="my_secret_key", algorithms=["HS256"])
