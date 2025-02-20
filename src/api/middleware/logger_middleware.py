# /src/api/middleware/logger_middleware.py

import time
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
        start_time = time.time()
        host = request.client.host if request.client else 'unknown'
        method = request.method
        url = str(request.url)

        log.info(f"Incoming Request: {host} - {method} {url} HTTP/1.1")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            status_code = response.status_code
            status_name = HTTPStatus(status_code).phrase

            log_message = f"{host} - {method} {url} HTTP/1.1 {status_code} {status_name} - {process_time:.2f}ms"

            if status_code >= 400:
                log.error(log_message)
            else:
                log.info(log_message)

            return response

        except Exception as error:
            error_message = (
                f"Error processing request {method} {url}: {str(error)}"
            )
            log.error(error_message)

            raise error
