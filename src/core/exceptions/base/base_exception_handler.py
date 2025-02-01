# src/core/exceptions/base/base_exception_handler.py

from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions.base.base_exception import BaseException


class BaseExceptionHandler:

    @staticmethod
    async def handler(request: Request, exc: BaseException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": str(exc.status_code),
                "status_name":
                "message": exc.detail,
            },
        )
