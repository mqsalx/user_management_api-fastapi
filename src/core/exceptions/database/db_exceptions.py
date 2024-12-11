from src.core.exceptions.base.base_exceptions import BaseApplicationException


class DatabaseConnectionException(BaseApplicationException):
    """Raised when the database connection cannot be established."""

    def __init__(self):
        super().__init__(
            "The connection to the database cannot be established, check the environment variables.",
            status_code=500,
        )
