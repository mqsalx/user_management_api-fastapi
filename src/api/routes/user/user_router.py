# /src/api/routes/user/user_router.py

from typing import List

from fastapi import APIRouter

from src.api.controllers.user.user_controller import UserController
from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO

router = APIRouter()


@router.post("", response_model=UserResponseDTO)
def create_user(
    request_data: UserRequestDTO,
    controller: UserController,
) -> UserResponseDTO:
    return controller.create_user(request_data)


@router.get("", response_model=UserResponseDTO)
def get_users(controller: UserController) -> List[UserResponseDTO]:
    return controller.get_users()


@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int, controller: UserController) -> UserResponseDTO:
    return controller.get_user(user_id)
