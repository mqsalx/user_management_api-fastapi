# /src/core/exceptions/api/middleware/jwt_middleware_exception.py

from src.core.exceptions.base.base_exception import BaseException
from fastapi import status


class UnauthorizedToken(BaseException):
    def __init__(self, message: str):
        status_code: int = status.HTTP_401_UNAUTHORIZED
        super().__init__(message, status_code)
