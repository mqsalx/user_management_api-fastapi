# /src/presentation/routes/user/get/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Core
from src.core.configurations import DatabaseConfig

# Domain
from src.domain.dtos.request.query.user import FindUserByUserIdQueryDTO

# Presentation
from src.presentation.controllers import UserController


class GetUserRouter:
    def __init__(self, user_router: APIRouter) -> None:
        self.__router: APIRouter = user_router
        self.__router.get(
            ""
        )(self.__call__)

    def __call__(
        self,
        query_params: FindUserByUserIdQueryDTO = Depends(),
        session_db: Session = Depends(DatabaseConfig().get_db),
    ) -> JSONResponse:
        """
        Endpoint that retrieves user(s).

        If a `user_id` is provided, it retrieves a specific user. Otherwise, it returns all users.
        """
        controller = UserController(session_db)
        return controller.find_user_controller(query_params)

    @property
    def router(self) -> APIRouter:
        return self.__router
