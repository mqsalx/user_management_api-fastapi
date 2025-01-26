# /src/core/exceptions/database/base_exceptions.py

from src.core.exceptions.base.base_exception import BaseException


class DatabaseConnectionException(BaseException):
    """
    Raised when the database connection cannot be established.
    """

    def __init__(self):
        super().__init__(
            "The connection to the database cannot be established, check the environment variables.",
            status_code=500,
        )
