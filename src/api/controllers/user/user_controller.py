# /src/api/controllers/user/user_controller.py

from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.db.database_configuration import DatabaseConfiguration
from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO
from src.infrastructure.repositories.user.user_repository import UserRepository
from src.usecases.user.user_usecase import UserUseCase


class UserController:
    def __init__(self, db: Session = Depends(DatabaseConfiguration().get_db)):
        self.__repository = UserRepository(db)
        self.__usecase = UserUseCase(self.__repository)

    def create_user(self, request_data: UserRequestDTO) -> UserResponseDTO:
        response_data = self.__usecase.create_user(request_data)
        return UserResponseDTO.model_validate(response_data)

    def get_user(self, user_id: int) -> UserResponseDTO:
        return self.__usecase.get_user(user_id)

    def get_users(self) -> List[UserResponseDTO]:
        return self.__usecase.get_users()
