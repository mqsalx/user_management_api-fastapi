# /src/presentation/routes/user/update/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Core
from src.core.configurations import DatabaseConfig

# Domain
from src.domain.dtos.request import (
    UpdateUserReqBodyDTO,
    UpdateUserReqPathDTO
)

# Presentation
from src.presentation.controllers.user.update import UpdateUserController


class UpdateUserRouter:
    """
    """
    def __init__(self, user_router: APIRouter) -> None:
        """
        """
        self.__router: APIRouter = user_router

        self.__router.patch(
            path="/{user_id}",
        )(self.__call__)

    def __call__(
        self,
        session_db: Session = Depends(DatabaseConfig().get_db),
        path: UpdateUserReqPathDTO = Depends(UpdateUserReqPathDTO.validate_path),
        body: UpdateUserReqBodyDTO = None
    ) -> JSONResponse:
        """
        Endpoint that updates user information.

        This Standalone Function updates the details of an existing user based on the provided user ID.

        Args:
            request (UpdateUserReqPathDTO): Data Transfer Object (DTO) containing
                the updated user details (e.g., name, email, password).
            session_db (Session): Database session dependency, injected via FastAPI's Depends.

        Returns:
            JSONResponse: A JSON response confirming the update.
        """
        controller = UpdateUserController(session_db)
        return controller(path, body)
