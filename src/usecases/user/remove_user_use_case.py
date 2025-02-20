# /src/usecases/user/delete_user_use_case.py


from sqlalchemy.orm import Session

from src.core.exceptions.base_exception import BaseException
from src.core.exceptions.user_exception import (
    UserNotFoundException,
)
from src.infrastructure.repository.user_repository import UserRepository
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class RemoveUserUseCase:

    def __init__(self, db: Session):
        self.__repository = UserRepository(db)

    def remove(self, user_id: str) -> None:

        try:

            self.__check_user_id(user_id)

            user = self.__repository.find_user(user_id)

            if not user:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            self.__repository.remove_user(user)
            self.__repository.database.commit()

            log.info(f"User deleted: id: {user_id}, name: {user.name}")

        except BaseException as error:
            log.error(f"Error in DeleteUserUseCase: {error}")
            raise

    def __check_user_id(self, user_id: str) -> None:
        if not user_id:
            raise UserNotFoundException(
                "User ID is required in the Query Params!"
            )
