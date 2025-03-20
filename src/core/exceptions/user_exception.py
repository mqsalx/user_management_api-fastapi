# /src/core/exceptions/user_exception.py

from fastapi import status

from src.core.exceptions.base_exception import BaseException


class UserNotFoundException(BaseException):
    """
    Class responsible for handling exceptions when a user is not found.

    This exception is raised when a user does not exist in the database.

    Class Args:
        message (str): The error message describing the issue.
        status_code (int): The HTTP status code associated with the exception (default: 404 Not Found).
    """

    def __init__(
        self, message: str, status_code: int = status.HTTP_404_NOT_FOUND
    ):
        """
        Constructor method for UserNotFoundException.

        Initializes the exception with a message and an optional status code.

        Args:
            message (str): The error message describing the exception.
            status_code (int, optional): The HTTP status code to return (default: 404 Not Found).
        """

        super().__init__(message, status_code)


class EmailAlreadyExistsException(BaseException):
    """
    Class responsible for handling exceptions when an email is already registered.

    This exception is raised when a user tries to create an account using an email
    that is already associated with an existing account.

    Class Args:
        message (str): The error message describing the issue.
        status_code (int): The HTTP status code associated with the exception (default: 400 Bad Request).
    """

    def __init__(
        self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        """
        Constructor method for EmailAlreadyExistsException.

        Initializes the exception with a message and an optional status code.

        Args:
            message (str): The error message describing the exception.
            status_code (int, optional): The HTTP status code to return (default: 400 Bad Request).
        """

        super().__init__(message, status_code)
