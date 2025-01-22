# /src/core/exceptions/usecases/auth/login_exception.py

from src.core.exceptions.base.base_exception import BaseException


class InvalidCredentialsException(BaseException):
    """Raised when a user is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)
