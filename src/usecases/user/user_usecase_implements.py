# /src/usecases/user/user_usecase.py

from datetime import datetime

from sqlalchemy.orm import Session

from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO
from src.core.exceptions.base.base_exception import BaseException
from src.core.exceptions.usecases.user.user_exception import (
    UserNotFoundException,
)
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.user_repository import UserRepository
from src.usecases.user.user_usecase_interface import UserUseCaseInterface
from src.utils.log.logger_util import LoggerUtil

log = LoggerUtil()


class UserUseCaseImplements(UserUseCaseInterface):
    """
    Creates a user. Transforms the DTO into an Entity and returns a response DTO.
    """

    def __init__(self, db: Session):
        self.__repository = UserRepository(db)

    def create_user(self, request: UserRequestDTO) -> UserResponseDTO:
        try:

            user_data = {
                "name": request.name,
                "email": request.email,
                "status": request.status,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            user = self.__repository.create_user(user_data)

            user_response = UserResponseDTO(
                id=user.id,
                name=user.name,
                email=user.email,
                status=user.status,
                created_at=user.created_at,
            )

            return user_response

        except BaseException as error:
            log.error(f"Error creating user: {error}")
            raise

    def get_users(self):
        users = self.__repository.get_users()
        return {
            UserResponseDTO.model_validate(users.__dict__) for user in users
        }

    def get_user(self, user_id: int) -> UserResponseDTO:
        user = self.__repository.get_user(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return UserResponseDTO.model_validate(user.__dict__)

    def to_response(self, user: UserModel):

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
