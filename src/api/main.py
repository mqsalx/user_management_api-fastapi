# /src/api/main.py

import time

import uvicorn
from fastapi import FastAPI

from src.api.routes.auth import login_router
from src.api.routes.user import user_router
from src.core.configurations.env_configuration import EnvConfiguration
from src.core.exceptions.base.base_exception import BaseException
from src.core.exceptions.base.base_exception_handler import (
    BaseExceptionHandler,
)
from src.infrastructure.db.database_configuration import DatabaseConfiguration
from src.usecases.scheduler_usecase import Scheduler

# Env variables Setup
API_HOST = EnvConfiguration().api_host
API_PORT = EnvConfiguration().api_port
API_VERSION = EnvConfiguration().api_version
URL_DATABASE = EnvConfiguration().db_url


def my_function():
    print("Testing...", time.strftime("%Y-%m-%d %H:%M:%S"))


my_scheduler_task = Scheduler()

my_scheduler_task.schedule_function(my_function, 5)

app = FastAPI()

DatabaseConfiguration().create_all()


app.add_exception_handler(BaseException, BaseExceptionHandler.handler)  # type: ignore

# app.add_middleware(JWTMiddleware)


routers = [(user_router.router, "/users"), (login_router.router, "/login")]

for router, prefix in routers:
    app.include_router(router, prefix=f"/api-{API_VERSION}{prefix}")


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
