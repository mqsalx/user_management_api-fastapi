# /src/core/middleware/auth/__init__.py

# flake8: noqa: E501

# PY
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

# Core
from src.core.configurations.environment import EnvConfig
from src.core.exceptions import InvalidTokenException

# Utils
from src.shared.utils import (
    AuthUtil,
    log,
    json_response
)

# Env variables Setup
API_VERSION: str = EnvConfig().api_version


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Class responsible for handling authentication middleware.

    This middleware intercepts incoming requests to enforce authentication by verifying
    JWT tokens. Requests to public paths are allowed without authentication.

    If a request does not contain a valid JWT token in the `Authorization` header,
    an HTTP 401 Unauthorized error is returned.

    Class Args:
        None
    """

    async def dispatch(self, request: Request, call_next):
        """
        Public asynchronous method responsible for processing incoming requests.

        This method verifies if a request requires authentication and checks
        the validity of the JWT token.

        Args:
            request (Request): The incoming HTTP request to be processed.
            call_next: The next middleware or route handler in the pipeline.

        Returns:
            Response: The processed response after authentication.

        Raises:
            HTTPException: If the authentication token is missing or invalid.
            Exception: If an unexpected error occurs during processing.
        """

        try:

            PUBLIC_PATHS = [
                "/api",
                f"/api/{API_VERSION}/auth/login",
                "/docs",
                "/openapi.json",
            ]
            print(API_VERSION)
            print(request.url.path)
            if request.url.path in PUBLIC_PATHS:
                response = await call_next(request)
                return response

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise InvalidTokenException("Token not provided!")

            access_token = auth_header.split(" ")[1]
            payload = AuthUtil.verify_token(access_token)

            session_id = dict(payload).get("session_id")

            if not session_id:
                raise InvalidTokenException("Invalid token structure!")

            request.state.access_token = access_token
            try:
                return await call_next(request)
            except Exception as error:
                log.error(f"Error in downstream handler: {str(error)}")
                return json_response(500, "Internal Server Error")

        except HTTPException as error:
            log.error(f"Token validation error: {error.detail}")
            return json_response(error.status_code, str(error.detail))

        except Exception as error:
            log.error(f"Unexpected error in JWT Middleware: {error}")
            return json_response(500, str(error))