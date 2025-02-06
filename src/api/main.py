# /src/api/main.py

import time

import uvicorn
from fastapi import FastAPI

from src.api.middleware.logger_middleware import LoggerMiddleware
from src.api.routes.user import user_router
from src.core.configurations.env_configuration import EnvConfiguration
from src.core.exceptions.base.base_exception import BaseException
from src.core.exceptions.exception_handler import ExceptionHandler
from src.usecases.scheduler_usecase import Scheduler
from src.utils.database.database_util import DatabaseUtil
from src.utils.dot_env.dot_env_util import DotEnvUtil
from src.utils.log.logger_util import LoggerUtil

app = FastAPI()
log = LoggerUtil()

# Env variables Setup
API_HOST = EnvConfiguration().api_host
API_PORT = EnvConfiguration().api_port
API_VERSION = EnvConfiguration().api_version


def my_function():
    log.info(f"Testing... {time.strftime("%Y-%m-%d %H:%M:%S")}")


my_scheduler_task = Scheduler()

my_scheduler_task.schedule_function(my_function, 5)

# Check ENV variables
DotEnvUtil().check_dot_env()

# Check Database Connection
DatabaseUtil().check_connection()

# Prepare Database
DatabaseUtil().setup_database()


app.add_exception_handler(BaseException, ExceptionHandler.handler)  # type: ignore

app.add_middleware(LoggerMiddleware)
# app.add_middleware(JWTMiddleware)


routers = [(user_router.router, "/users")]
# routers = [(user_router.router, "/users"), (login_router.router, "/login")]

for router, prefix in routers:
    app.include_router(router, prefix=f"/api-{API_VERSION}{prefix}")


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
