# /src/utils/response/response_util.py

from http import HTTPStatus
from typing import Dict

from fastapi.responses import JSONResponse


class ResponseUtil:

    def json_response(
        self, status_code: int, message: str, data: Dict[str, str]
    ) -> JSONResponse:

        response = JSONResponse(
            status_code=status_code,
            content={
                "status_code": str(status_code),
                "status_name": HTTPStatus(status_code).phrase,
                "message": message,
                "data": data,
            },
        )

        return response
