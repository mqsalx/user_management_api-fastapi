# src/core/exceptions/base/base_exception_handler.py

from http import HTTPStatus

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ExceptionHandler:

    @staticmethod
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        """Handles generic HTTP exceptions in FastAPI."""
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
    ) -> JSONResponse:

        for error in exc.errors():
            if error["type"] == "json_invalid":
                status_code = status.HTTP_400_BAD_REQUEST
                return JSONResponse(
                    status_code=status_code,
                    content={
                        "status_code": str(status_code),
                        "status_name": HTTPStatus(status_code).phrase,
                        "message": "Invalid JSON format. Ensure the request body is correctly formatted."
                    },
                )

        return JSONResponse(
            status_code=422,
            content={
                "status_code": "422",
                "status_name": HTTPStatus(422).phrase,
                "message": "Validation error in request body.",
                "details": exc.errors(),
            },
        )
