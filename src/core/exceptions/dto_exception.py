# /src/core/exceptions/dto_exception.py

from fastapi import status

from src.core.exceptions.base_exception import BaseException


class OnlyAcceptsValuesException(BaseException):

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        super().__init__(
            message,
            status_code,
        )


class InvalidExtraFieldsException(BaseException):

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        super().__init__(
            message,
            status_code,
        )


class MissingRequiredFieldsException(BaseException):

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        super().__init__(
            message,
            status_code,
        )
