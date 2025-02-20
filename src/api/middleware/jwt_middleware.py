from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.configurations.env_configuration import EnvConfiguration
from src.utils.jwt_util import verify_token
from src.utils.logger_util import LoggerUtil

# Env variables Setup
API_VERSION = EnvConfiguration().api_version

# Log variables Setup
log = LoggerUtil()


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            # 🔹 Exceções para endpoints públicos
            if request.url.path in [
                f"/api-{API_VERSION}/login",
                "/docs",
                "/openapi.json",
            ]:
                return await call_next(request)

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=401, detail="Token not provided!"
                )

            token = auth_header.split(" ")[1]

            try:
                verify_token(token)
            except ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expired!")
            except InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token!")

            return await call_next(request)

        except HTTPException as http_exc:
            log.error(f"Token validation error: {http_exc.detail}")
            return self.__json_response(http_exc)

        except Exception as error:
            log.error(f"Unexpected error during token validation: {error}")
            return self.__json_response(
                HTTPException(status_code=401, detail=str(error))
            )

    def __json_response(self, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": str(exc.status_code),
                "status_name": HTTPStatus(exc.status_code).phrase,
                "message": exc.detail,
            },
        )
