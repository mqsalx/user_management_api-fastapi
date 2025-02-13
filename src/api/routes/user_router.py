# /src/api/routes/user_router.py


from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.api.controllers.user_controller import UserController
from src.core.dtos.user_dto import UserRequestDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

router = APIRouter()


@router.post("", response_model=None)
def create_user_router(
    request: UserRequestDTO,
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    controller = UserController(db)
    return controller.create_user_handler(request)


@router.delete("", response_model=None)
def delete_user_router(
    user_id: int = Query(None, description="User ID to delete"),
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    controller = UserController(db)
    return controller.delete_user_handler(user_id)


@router.get("", response_model=None)
def get_user(
    user_id: int | None = Query(None, description="User ID (optional)"),
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:

    controller = UserController(db)
    return controller.get_user_handler(user_id)
