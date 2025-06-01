# /src/presentation/routes/user/remove/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Core
from src.core.configurations import DatabaseConfig

# Domain
from src.domain.dtos.request.path.user import RemoveUserByUserIdReqPathDTO

# Presentation
from src.presentation.controllers import UserController


class RemoveUserRouter:
    """
    """
    def __init__(self, user_router: APIRouter) -> None:
        """
        """
        self.__router: APIRouter = user_router

        self.__router.delete(
            path="/{user_id}",
        )(self.__call__)

    def __call__(
        self,
        path: RemoveUserByUserIdReqPathDTO = Depends(),
        session_db: Session = Depends(DatabaseConfig().get_db),
    ) -> JSONResponse:
        """
        Endpoint that handles user creation.

        This method processes user registration requests and returns a confirmation
        message upon successful user creation.
        """
        controller = UserController(session_db)
        return controller.remove_user_controller(path)

    @property
    def router(self) -> APIRouter:
        """
        """
        return  self.__router