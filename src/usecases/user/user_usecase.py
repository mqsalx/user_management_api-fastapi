# /app/usecases/user_usecase.py

from src.adapters.repositories.user_repository import UserRepository
from adapters.validators.user.user_validator import UserValidator
from src.core.exceptions.usecases.user.user_exceptions import (
    EmailAlreadyExistsException,
    UserNotFoundException,
)
from dtos.user.user_dto import UserCreateDTO, UserResponseDTO


class UserUseCase:
    def __init__(
        self, user_repo: UserRepository, user_validator: UserValidator
    ):
        self.user_repo = user_repo
        self.user_validator = user_validator

    def create_user(self, user_data: UserCreateDTO) -> UserResponseDTO:
        if self.user_validator.email_exists(user_data.email):
            raise EmailAlreadyExistsException(user_data.email)
        user = self.user_repo.create_user(user_data)
        return UserResponseDTO.model_validate(user.__dict__)

    def get_user(self, user_id: int) -> UserResponseDTO:
        user = self.user_repo.get_user(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return UserResponseDTO.model_validate(user.__dict__)

    def get_users(self):
        users = self.user_repo.get_users()
        return [
            UserResponseDTO.model_validate(user.__dict__) for user in users
        ]
