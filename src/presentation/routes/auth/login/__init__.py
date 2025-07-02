# /src/presentation/routes/auth/login/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Core
from src.core.configurations import DatabaseConfig

# Domain
from src.domain.dtos import LoginRequestDTO

# Presentation
from src.presentation.controllers import (
    ILoginController,
    LoginControllerImpl
)


class LoginRouter():
    """
    """
    def __init__(self, user_router: APIRouter) -> None:
        """
        """
        self.__router: APIRouter = user_router

        self.__router.post(
            path="/login",
            description=""
        )(self.__call__)

    def __call__(
        self,
        session_db: Session = Depends(DatabaseConfig().get_db),
        body: LoginRequestDTO = None
    ) -> JSONResponse:
        """
        Endpoint that handles user creation.

        This method processes user registration requests and returns
            a confirmation message upon successful user creation.
        """
        controller: ILoginController  = LoginControllerImpl(session_db=session_db)
        return controller(body)
