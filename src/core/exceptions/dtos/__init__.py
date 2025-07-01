# /src/core/exceptions/dtos/__init__.py

# flake8: noqa: E501

from fastapi import status

from src.core.exceptions.base import BaseHTTPException


class OnlyAcceptsValuesException(BaseHTTPException):
    """
    Class responsible for handling exceptions when a field only accepts specific values.

    This exception is raised when an input field receives an empty or invalid value
    that is not among the accepted options.

    Class Args:
        message (str): The error message describing the validation failure.
        status_code (int): The HTTP status code associated with the exception (default: 422 Unprocessable Entity).
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        """
        Constructor method for OnlyAcceptsValuesException.

        Initializes the exception with a message and an optional status code.

        Args:
            message (str): The error message describing the exception.
            status_code (int, optional): The HTTP status code to return (default: 422 Unprocessable Entity).
        """

        super().__init__(message, status_code)


class InvalidExtraFieldsException(BaseHTTPException):
    """
    Class responsible for handling exceptions when extra fields are provided.

    This exception is raised when an unexpected field is included in the request,
    ensuring that only allowed fields are processed.

    Class Args:
        message (str): The error message describing the validation failure.
        status_code (int): The HTTP status code associated with the exception (default: 422 Unprocessable Entity).
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        """
        Constructor method for InvalidExtraFieldsException.

        Initializes the exception with a message and an optional status code.

        Args:
            message (str): The error message describing the exception.
            status_code (int, optional): The HTTP status code to return (default: 422 Unprocessable Entity).
        """

        super().__init__(message, status_code)


class MissingRequiredFieldsException(BaseHTTPException):
    """
    Class responsible for handling exceptions when required fields are missing.

    This exception is raised when one or more mandatory fields are not included
    in the request, enforcing data integrity.

    Class Args:
        message (str): The error message describing the validation failure.
        status_code (int): The HTTP status code associated with the exception (default: 422 Unprocessable Entity).
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        """
        Constructor method for MissingRequiredFieldsException.

        Initializes the exception with a message and an optional status code.

        Args:
            message (str): The error message describing the exception.
            status_code (int, optional): The HTTP status code to return (default: 422 Unprocessable Entity).
        """

        super().__init__(message, status_code)


class InvalidValueInFieldException(BaseHTTPException):
    """
    Class responsible for handling exceptions when a field is present but contains an invalid value.

    This exception is typically used in scenarios where fields are provided
    (e.g., via query parameters or request body) but their values do not meet
    semantic validation rules, such as being blank, only whitespace, or not matching
    the expected format.

    Class Args:
        message (str): The error message describing the validation failure.
        status_code (int): The HTTP status code associated with the exception (default: 422 Unprocessable Entity).
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ) -> None:
        """
        Constructor method for MissingRequiredFieldsException.

        Initializes the exception with a message and an optional status code.

        Args:
            message (str): The error message describing the exception.
            status_code (int, optional): The HTTP status code to return (default: 422 Unprocessable Entity).
        """

        super().__init__(message, status_code)
