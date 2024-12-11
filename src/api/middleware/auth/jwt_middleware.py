from fastapi import HTTPException, Request
from fastapi.middleware.base import BaseHTTPMiddleware

from utils.auth.jwt_utils import verify_token


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware para verificar o token JWT em todas as requisições."""

    async def dispatch(self, request: Request, call_next):
        # Ignorar rotas públicas
        if request.url.path in ["/api/login", "/docs", "/openapi.json"]:
            return await call_next(request)

        # Obter o token do cabeçalho Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token não fornecido")

        token = auth_header.split(" ")[1]
        try:
            verify_token(token)  # Valida o token
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

        # Continua para a próxima etapa da requisição
        return await call_next(request)
        return await call_next(request)
