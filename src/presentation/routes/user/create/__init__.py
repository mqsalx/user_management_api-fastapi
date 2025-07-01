# /src/presentation/routes/user/create/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Core
from src.core.configurations import DatabaseConfig

# Domain
from src.domain.dtos import CreateUserReqBodyDTO

# Presentation
from src.presentation.controllers import CreateUserController


class CreateUserRouter:
    """
    """
    def __init__(self, user_router: APIRouter) -> None:
        """
        """
        self.__router: APIRouter = user_router

        self.__router.post(
            path="",
            description="",
            response_model=None
        )(self.__call__)

    def __call__(
        self,
        session_db: Session = Depends(DatabaseConfig().get_db),
        body: CreateUserReqBodyDTO = None,
        background_tasks: BackgroundTasks = None
    ) -> JSONResponse:
        """
        Endpoint that handles user creation.

        This method processes user registration requests and returns
            a confirmation message upon successful user creation.
        """
        controller = CreateUserController(session_db)
        return controller(body, background_tasks)
