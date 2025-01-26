# /src/core/exceptions/usecases/user/user_exception.py

from src.core.exceptions.base.base_exception import BaseException


class UserNotFoundException(BaseException):
    """Raised when a user is not found in the database."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class EmailAlreadyExistsException(BaseException):
    """Raised when a user tries to create an account with an existing email."""

    def __init__(self, message: str):

        super().__init__(message, status_code=400)
