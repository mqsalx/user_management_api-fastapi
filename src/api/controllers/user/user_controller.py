# /src/api/controllers/user/user_controller.py

from typing import List

from sqlalchemy.orm import Session

from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO
from src.infrastructure.repositories.user.user_repository import UserRepository
from src.usecases.user.user_usecase import UserUseCase


class UserController:
    def __init__(self, db: Session):
        self.__db = db
        self.__repository = UserRepository(self.__db)
        self.__usecase = UserUseCase(self.__repository)

    def create_user(self, request_data: UserRequestDTO) -> UserResponseDTO:
        response_data = self.__usecase.create_user(request_data)
        return UserResponseDTO.model_validate(response_data)

    def get_users(self) -> UserResponseDTO:
        return self.__usecase.get_users()

    def get_user(self, user_id: int) -> UserResponseDTO:
        return self.__usecase.get_user(user_id)
