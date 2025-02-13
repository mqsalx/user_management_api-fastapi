# /src/api/middleware/logger_middleware.py


from http import HTTPStatus

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class LoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next) -> Response:
        """
        # TODO: define docstrings
        """
        try:

            response = await call_next(request)
            host = request.client.host
            method = request.method
            url = str(request.url)
            status_code = response.status_code
            status_name = HTTPStatus(status_code).phrase
            log_message = (
                f"{host} - {method} {url} HTTP/1.1 {status_code} {status_name}"
            )

            if status_code >= 400:
                log.error(log_message)
            return response

        except Exception as error:
            log.error(f"Error: {str(error)}")
            raise error
