# /src/core/exceptions/database/base_exceptions.py

from fastapi import status

from src.core.exceptions.base.base_exception import BaseException


class DatabaseConnectionException(BaseException):
    """
    Raised when the database connection cannot be established.
    """

    def __init__(
        self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED
    ):
        super().__init__(
            message,
            status_code,
        )


class DatabaseInvalidConfigurationException(BaseException):
    """
    # TODO: define docstrings
    """

    def __init__(
        self, message: str, status_code: int = status.HTTP_404_NOT_FOUND
    ):
        super().__init__(
            message,
            status_code,
        )
