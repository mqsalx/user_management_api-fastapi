# /src/usecases/user/create_user_use_case.py

from datetime import datetime
from typing import Dict

from sqlalchemy.orm import Session

from src.core.dtos.user_dto import UserRequestDTO
from src.core.exceptions.base_exception import BaseException
from src.core.exceptions.user_exception import (
    EmailAlreadyExistsException,
)
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.user_repository import UserRepository
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class CreateUserUseCase:
    """
    Creates a user. Transforms the DTO into an Entity and returns a response DTO.
    """

    def __init__(self, db: Session):
        self.__repository = UserRepository(db)

    def create(self, request: UserRequestDTO) -> dict[str, str]:
        try:

            self.__check_user_email(request.email)

            user = self.__repository.create_user(
                name=request.name,
                email=request.email,
                status=request.status,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            return self.__response(user)

        except (Exception, BaseException) as error:
            self.__repository.database.rollback()
            log.error(f"Error during the user creation process: {error}")
            raise error

    def __check_user_email(self, user_email: str) -> None:
        if self.__repository.get_user_email(user_email):
            raise EmailAlreadyExistsException(
                f"User with email {user_email} already exists!"
            )
        return None

    def __response(self, user: UserModel) -> Dict[str, str]:
        return {
            "id": str(user.id),
            "name": str(user.name),
            "email": str(user.email),
        }
