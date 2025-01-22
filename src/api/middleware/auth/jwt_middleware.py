# /src/api/middleware/auth/jwt_middleware.py

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.auth.jwt_util import verify_token


class JWTMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check the JWT token on all requests.
    """

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/api/login", "/docs", "/openapi.json"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized!")

        token = auth_header.split(" ")[1]

        try:
            verify_token(token)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

        return await call_next(request)
