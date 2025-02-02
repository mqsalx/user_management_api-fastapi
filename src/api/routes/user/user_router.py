# /src/api/routes/user/user_router.py


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.controllers.user_controller import UserController
from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

router = APIRouter()


@router.post("", response_model=UserResponseDTO)
def create_user(
    request: UserRequestDTO,
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> UserResponseDTO:
    controller = UserController(db)
    return controller.create_user(request)


@router.get("", response_model=UserResponseDTO)
def get_users() -> UserResponseDTO:
    controller = UserController()
    return controller.get_users()


@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int) -> UserResponseDTO:
    controller = UserController()
    return controller.get_user(user_id)
