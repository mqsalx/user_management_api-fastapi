# /src/api/main.py


import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.middleware.auth.jwt_middleware import JWTMiddleware
from src.api.routes.auth import login_router
from src.api.routes.user import user_router
from src.core.configurations.env_configuration import EnvConfiguration
from core.exceptions.base.base_exception import BaseException
from src.infrastructure.db.database_configuration import DatabaseConfiguration

# Env variables Setup
API_HOST = EnvConfiguration().api_host
API_PORT = EnvConfiguration().api_port
API_PREFIX = EnvConfiguration().api_prefix


app = FastAPI()

app.add_middleware(JWTMiddleware)


@app.exception_handler(BaseException)
async def base_exception_handler(
    request: Request, exc: BaseException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


routers = [(user_router.router, "/users"), (login_router.router, "/login/")]

for router, prefix in routers:
    app.include_router(router, prefix=f"/api-{API_PREFIX}{prefix}")

DatabaseConfiguration().create_all()

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
