# /src/presentation/routes/auth/logout/__init__.py

# flake8: noqa: E501

# PY
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Core
from src.core.configurations import DatabaseConfig

# Presentation
from src.presentation.controllers import LogoutController


class LogoutRouter:
    """
    """
    def __init__(self, user_router: APIRouter) -> None:
        self.__router: APIRouter = user_router

        self.__router.post(
            path="/logout",
            description=""
        )(self.__call__)

    def __call__(
        self,
        request: Request,
        session_db: Session = Depends(DatabaseConfig().get_db),
    ) -> JSONResponse:
        """
        """

        controller = LogoutController(session_db)
        return controller(request)
