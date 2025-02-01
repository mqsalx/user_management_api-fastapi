# /src/core/exceptions/base/base_exception.py

from fastapi import HTTPException, status


class BaseException(HTTPException):
    """Base class for all application-specific exceptions."""

    def __init__(
        self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        super().__init__(status_code=status_code, detail=message)
