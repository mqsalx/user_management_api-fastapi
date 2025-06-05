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
from src.presentation.controllers.user.find import FindUserController

class GetUserRouter:
    def __init__(self, user_router: APIRouter) -> None:
        self.__router: APIRouter = user_router
        self.__router.get(
            ""
        )(self.__call__)

    def __call__(
        self,
        session_db: Session = Depends(DatabaseConfig().get_db),
        query: FindUserByUserIdQueryDTO = Depends()
    ) -> JSONResponse:
        """
        Endpoint that retrieves user(s).

        If a `user_id` is provided, it retrieves a specific user. Otherwise, it returns all users.
        """
        controller = FindUserController(session_db)
        return controller(query)
