# /src/shared/presentation/schemas/response/base/__init__.py

# PY
import datetime
from dataclasses import asdict, is_dataclass
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, Union

from fastapi.responses import JSONResponse


class BaseResponse:
    """
    Class responsible for handling JSON responses.

    This class provides a method to generate consistent JSON responses with
    status codes, messages, and optional data.

    Class Args:
        status_code (int): HTTP status code.
        message (str | None): Optional response message.
        data (Any | None): Data payload, can be Pydantic model,
            dataclass ou dict.
        pagination (Any | None): Optional pagination metadata.
    """

    def __new__(
        cls,
        status_code: int,
        message: str | None = None,
        data: Any | None = None,
        pagination: Any | None = None,
    ) -> JSONResponse:
        """
        Create a new JSONResponse instance using provided parameters.

        Args:
            status_code (int): HTTP status code.
            message (str | None): Optional response message.
            data (Any | None): Data payload, can be Pydantic model,
                dataclass ou dict.
            pagination (Any | None): Optional pagination metadata.

        Returns:
            JSONResponse: A FastAPI-compatible response object.
        """

        instance = super().__new__(cls)

        return instance.__call__(
            status_code=status_code,
            message=message,
            data=data,
            pagination=pagination,
        )

    def __call__(
        self,
        status_code: int,
        message: str | None = None,
        data: Any | None = None,
        pagination: Any | None = None,
    ) -> JSONResponse:
        """
        Builds the content dictionary and returns it as a JSONResponse.

        Args:
            status_code (int): HTTP status code.
            message (str | None): Optional response message.
            data (Any | None): Data payload, can be Pydantic model,
                dataclass ou dict.
            pagination (Any | None): Optional pagination metadata.

        Returns:
            JSONResponse: A consistent API response.
        """
        response_content: Dict[str, Union[str, Dict[str, str]]] = {
            "status_code": str(status_code),
            "status_name": HTTPStatus(status_code).phrase,
        }

        if message is not None:
            response_content["message"] = message

        def _serialize(value: Any) -> Any:
            if isinstance(value, Enum):
                return value.value
            elif isinstance(
                value, (datetime.datetime, datetime.date, datetime.time)
            ):
                return value.isoformat()
            elif hasattr(value, "model_dump"):
                return value.model_dump()
            elif hasattr(value, "dict"):
                return value.dict()
            elif is_dataclass(value):
                return {
                    k: _serialize(v)  # Recursivo p/ Enum dentro de dataclass
                    for k, v in asdict(value).items()
                }
            elif isinstance(value, list):
                return [_serialize(item) for item in value]
            elif isinstance(value, dict):
                return {k: _serialize(v) for k, v in value.items()}
            return value

        if data is not None:
            response_content["data"] = _serialize(data)

        if pagination is not None:
            response_content["pagination"] = _serialize(pagination)

        return JSONResponse(status_code=status_code, content=response_content)
