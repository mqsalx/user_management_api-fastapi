# /src/usecases/user/user_usecase.py

from src.core.entities.user.user_entity import UserEntity
from src.core.exceptions.base.base_exception import BaseException
from core.exceptions.usecases.user.user_exception import (
    EmailAlreadyExistsException,
    UserNotFoundException,
)
from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO
from src.infrastructure.repositories.user.user_repository import UserRepository
from src.utils.log.console_logger_util import ConsoleLoggerUtil

CONSOLE_LOGGER_ERROR = ConsoleLoggerUtil().log_error


class UserUseCase:
    """
    Creates a user. Transforms the DTO into an Entity and returns a response DTO.
    """

    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def create_user(self, data: UserRequestDTO) -> UserResponseDTO:

        try:
            if self.__repository.get_email(data.email):
                raise EmailAlreadyExistsException(data.email)

            entity = UserEntity(
                name=data.name,
                email=data.email,
                status=data.status,
            )

            return self.__repository.create_user(entity)
        except BaseException as error:
            CONSOLE_LOGGER_ERROR(f"Error creating user: {error}")
            raise

    def get_user(self, user_id: int) -> UserResponseDTO:
        user = self.__repository.get_user(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return UserResponseDTO.model_validate(user.__dict__)

    def get_users(self):
        users = self.__repository.get_users()
        return [
            UserResponseDTO.model_validate(user.__dict__) for user in users
        ]
