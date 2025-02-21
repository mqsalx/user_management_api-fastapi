from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.configurations.env_configuration import EnvConfiguration
from src.utils.jwt_util import JWTUtil
from src.utils.logger_util import LoggerUtil
from src.utils.response_util import ResponseUtil

# Env variables Setup
API_VERSION = EnvConfiguration().api_version

# Utils Setup
json_response = ResponseUtil().json_response
log = LoggerUtil()


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:

            PUBLIC_PATHS = [
                f"/api-{API_VERSION}/login",
                f"/api-{API_VERSION}/register",
                "/docs",
                "/openapi.json",
            ]

            if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
                response = await call_next(request)
                return response

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=401, detail="Token not provided!"
                )

            token = auth_header.split(" ")[1]

            JWTUtil.verify_token(token)

            response = await call_next(request)

            if response is None:
                return json_response(500, "Internal server error")

            return response

        except HTTPException as error:
            log.error(f"Token validation error: {error.detail}")
            return json_response(error.status_code, str(error.detail))

        except Exception as error:
            log.error(f"Unexpected error in JWT Middleware: {error}")
            return json_response(500, str(error))
