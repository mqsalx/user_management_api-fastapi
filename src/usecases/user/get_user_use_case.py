# /src/usecases/user/get_user_use_case.py


from typing import Dict, List, Optional, Union

from sqlalchemy.orm import Session

from src.core.exceptions.user_exception import (
    UserNotFoundException,
)
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.user_repository import UserRepository
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class GetUserUseCase:
    def __init__(self, db: Session):
        self.__repository = UserRepository(db)

    def get(
        self, user_id: Optional[int] = None
    ) -> Union[Dict[str, str], List[Dict[str, str]]]:

        try:
            if user_id is None:
                users = self.__repository.get_users()

                if users is None:
                    log.info("No users found!")
                    return []
                return self.__response_list(users)
            else:
                user = self.__repository.get_user(user_id)
                if not user:
                    raise UserNotFoundException(
                        f"User with ID {user_id} is invalid or incorrect!"
                    )

                return self.__response(user)

        except Exception as error:
            log.error(f"Error in GetUserUseCase: {error}")
            raise

    def __response(self, user: UserModel) -> Dict[str, str]:

        return {
            "id": str(user.id),
            "name": str(user.name),
            "email": str(user.email),
        }

    def __response_list(self, users: List[UserModel]) -> List[Dict[str, str]]:

        return [self.__response(user) for user in users]
