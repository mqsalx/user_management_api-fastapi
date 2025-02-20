# /src/core/exceptions/login_exception.py

from fastapi import status

from src.core.exceptions.base_exception import BaseException


class InvalidCredentialsException(BaseException):
    """Raised when a user is not found in the database."""

    def __init__(
        self, message: str, status_code: int = status.HTTP_404_NOT_FOUND
    ):
        super().__init__(message, status_code)


class ErrorTokenException(BaseException):
    """Raised when a user is not found in the database."""

    def __init__(
        self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(message, status_code)
