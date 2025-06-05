# /src/main.py

# flake8: noqa: E501

"""
Main module responsible for initializing and running the FastAPI application.

This module sets up the API, middleware, exception handlers, and scheduled tasks.
It also checks environment variables and the database connection before starting
the server.
"""

# PY
import time

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

# Core
from src.core.configurations import (
    EnvConfig,
    SchedulerConfig
)
from src.core.handlers.exception import ExceptionHandler
from src.core.middleware import (
    AuthMiddleware,
    LoggerMiddleware
)

# Presentation
from src.presentation.routes import ApiRouter

# Utils
from src.utils import (
    DatabaseUtil,
    DotEnvUtil,
    log,
    MessageUtil
)

# Env variables Setup
API_HOST = EnvConfig().api_host
API_NAME = EnvConfig().api_name
API_PORT = EnvConfig().api_port
API_VERSION = EnvConfig().api_version

app = FastAPI(
    title=API_NAME,
    version=API_VERSION,
    description=f"{API_NAME} API documentation!"
)


def my_function():
    """
    Standalone function responsible for testing scheduled tasks.

    This function logs a test message with the current timestamp.

    Args:
        None

    Returns:
        None
    """

    log.info(f"Testing... {time.strftime("%Y-%m-%d %H:%M:%S")}")


my_scheduler_task = SchedulerConfig()

# my_scheduler_task.schedule_function(my_function, 5)

app.add_exception_handler(HTTPException, ExceptionHandler.http_exception_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, ExceptionHandler.json_decode_error_handler)  # type: ignore

app.add_middleware(LoggerMiddleware)
app.add_middleware(AuthMiddleware)

api_router: APIRouter = ApiRouter().router

app.include_router(api_router, prefix=f"/api")

if __name__ == "__main__":
    """
    Application startup sequence.

    This section ensures that essential configurations are checked before
    running the FastAPI server.
    """

    # On Startup Message
    MessageUtil().on_startup()

    # Check ENV variables
    DotEnvUtil().check_dot_env()

    # Check Database Connection
    DatabaseUtil().check_connection()

    width = 80
    border = "=" * width

    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
    )
