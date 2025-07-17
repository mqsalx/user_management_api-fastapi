# /src/core/handlers/exception/__init__.py

# flake8: noqa: E501

from http import HTTPStatus

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ExceptionHandler:
    """
    Class responsible for handling application-wide exceptions.

    This class provides static methods to handle different types of HTTP exceptions
    and request validation errors in a structured manner.

    Class Args:
        None
    """

    @staticmethod
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse | None:
        """
        Static asynchronous method responsible for handling generic HTTP exceptions.

        This method intercepts `HTTPException` errors raised in FastAPI and returns
        a structured JSON response with relevant status codes and messages.

        Args:
            request (Request): The incoming HTTP request that triggered the exception.
            exc (HTTPException): The exception instance containing status and detail.

        Returns:
            JSONResponse | None: A JSON response containing the error details.
        """

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": str(exc.status_code),
                "status_name": HTTPStatus(exc.status_code).phrase,
                "message": exc.detail,
            },
        )

    @staticmethod
    async def json_decode_error_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse | None:
        """
        Static asynchronous method responsible for handling JSON decoding errors.

        This method intercepts `RequestValidationError` caused by invalid JSON format
        in the request body and returns a structured JSON response.

        Args:
            request (Request): The incoming HTTP request that triggered the exception.
            exc (RequestValidationError): The exception instance containing validation errors.

        Returns:
            JSONResponse | None: A JSON response containing the error details.
        """
        status_code = None
        message = None

        for error in exc.errors():
            error_type = error.get("type")
            loc = error.get("loc", [])
            input_value = error.get("input", None)
            msg = error.get("msg", "Invalid input")

            # Origin (ex: 'query', 'body', 'path')
            source = loc[0] if loc else "unknown"

            # Field (ex: 'user_id')
            field = loc[1] if len(loc) > 1 else "unknown"

            if error_type == "json_invalid":
                status_code = status.HTTP_400_BAD_REQUEST
                message = "Invalid JSON format. Ensure the request body is correctly formatted."
                break

            elif error_type == "missing":
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                message = (
                    f"The field '{field}' from '{source}' is required and was not provided."
                )
                break

            elif error_type == "enum":
                allowed_values = error.get("ctx", {}).get("expected", [])
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                message = (
                    f"The field '{field}' from '{source}' must be one of {allowed_values}. "
                    f"Received: '{input_value}'."
                )
                break

            elif error_type == "int_parsing":
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                message = (
                    f"The field '{field}' from '{source}' must be an integer. "
                    f"Received: '{input_value}' ({type(input_value).__name__})."
                )
                break
            print(f"Unhandled error type: {error_type} for field '{field}' in {source}")

        # fallback for other errors not explicitly dealt with
        if not status_code:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            message = "Validation failed for one or more fields."

        return JSONResponse(
            status_code=status_code,
            content={
                "status_code": str(status_code),
                "status_name": HTTPStatus(status_code).phrase,
                "message": message,
            },
        )
