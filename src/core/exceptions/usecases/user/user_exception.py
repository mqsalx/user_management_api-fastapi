# /src/core/exceptions/usecases/user/user_exception.py

from fastapi import status

from src.core.exceptions.base.base_exception import BaseException


class UserNotFoundException(BaseException):
    """Raised when a user is not found in the database."""

    def __init__(
        self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(message, status_code)


class EmailAlreadyExistsException(BaseException):
    """Raised when a user tries to create an account with an existing email."""

    def __init__(
        self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):

        super().__init__(message, status_code)
