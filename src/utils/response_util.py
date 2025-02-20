# /src/utils/response_util.py

from http import HTTPStatus
from typing import Dict, Union

from fastapi.responses import JSONResponse


class ResponseUtil:
    def json_response(
        self,
        status_code: int,
        message: str | None = None,
        data: Dict[str, str] | None = None,
    ) -> JSONResponse:

        response_content: Dict[str, Union[str, Dict[str, str]]] = {
            "status_code": str(status_code),
            "status_name": HTTPStatus(status_code).phrase,
        }

        if message is not None:
            response_content["message"] = message

        if data is not None:
            response_content["data"] = data

        return JSONResponse(status_code=status_code, content=response_content)
