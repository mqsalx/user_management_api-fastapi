# /src/api/routes/user_router.py


from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.api.controllers.user_controller import UserController
from src.core.dtos.user_dto import CreateUserRequestDTO, UpdateUserRequestDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

router = APIRouter()


@router.post("", response_model=None)
def create_user_router(
    request: CreateUserRequestDTO,
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    controller = UserController(db)
    return controller.create_user_controller(request)


@router.delete("", response_model=None)
def remove_user_router(
    user_id: str = Query(None, description="User ID to delete."),
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    controller = UserController(db)
    return controller.remove_user_controller(user_id)


@router.get("", response_model=None)
def find_user_router(
    user_id: str | None = Query(None, description="User ID (optional) to find."),
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:

    controller = UserController(db)
    return controller.find_user_controller(user_id)


@router.patch("/{user_id}", response_model=None)
def update_user_router(
    user_id: str,
    request: UpdateUserRequestDTO,
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    controller = UserController(db)
    return controller.update_user_controller(user_id, request)
