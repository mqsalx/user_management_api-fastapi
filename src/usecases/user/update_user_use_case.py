# /src/usecases/user/update_user_use_case.py

from typing import Dict

from sqlalchemy.orm import Session

from src.core.dtos.user_dto import UpdateUserRequestDTO
from src.core.exceptions.base_exception import BaseException
from src.core.exceptions.user_exception import UserNotFoundException
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.user_repository import UserRepository
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class UpdateUserUseCase:
    """
    Updates an existing user only with the provided fields.
    """

    def __init__(self, db: Session):
        self.__repository = UserRepository(db)

    def update(
        self, user_id: str, request: UpdateUserRequestDTO
    ) -> dict[str, str]:
        try:
            if not user_id:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            user = self.__repository.find_user(user_id)

            if not user:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            update_data = request.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)

            self.__repository.database.commit()
            self.__repository.database.refresh(user)

            return self.__response(user)

        except (Exception, BaseException) as error:
            self.__repository.database.rollback()
            log.error(f"Error during the user update process: {error}")
            raise error

    def __response(self, user: UserModel) -> Dict[str, str]:
        return {
            "user_id": str(user.user_id),
            "name": str(user.name),
            "email": str(user.email),
        }
