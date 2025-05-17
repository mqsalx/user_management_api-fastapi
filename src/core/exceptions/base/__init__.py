# /src/core/exceptions/base/__init__.py

# flake8: noqa: E501, F401

from fastapi import HTTPException, status


class BaseException(HTTPException):
    """
    Class responsible for the base exception used in the application.

    This class serves as the parent exception for all custom exceptions in the system.
    It extends FastAPI's `HTTPException`, allowing structured error handling.

    Class Args:
        message (str): The error message describing the exception.
        status_code (int): The HTTP status code associated with the exception (default: 400 Bad Request).

    """

    def __init__(
        self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        """
        Constructor method that initializes the BaseException with a message and an optional status code.

        Args:
            message (str): The error message describing the exception.
            status_code (int, optional): The HTTP status code to return (default: 400 Bad Request).
        """

        super().__init__(status_code=status_code, detail=message)
