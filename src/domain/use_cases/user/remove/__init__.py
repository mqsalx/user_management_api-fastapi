# /src/domain/use_cases/user/remove/__init__.py

# flake8: noqa: E501

# PY
from sqlalchemy.orm import Session

# Core
from src.core.exceptions import (
    BaseException,
    UserNotFoundException
)

# Data
from src.data.repositories import UserRepository

# Domain
from src.domain.dtos.request.path.user import RemoveUserByUserIdReqPathDTO

# utils
from src.utils import LoggerUtil

log = LoggerUtil()


class RemoveUserUseCase:
    """
    Class responsible for handling the user removal use case.

    This class manages the process of deleting a user from the system.

    Class Args:
        session_db (Session): The database session required for executing queries.
    """

    def __init__(self, session_db: Session):
        """
        Constructor method for RemoveUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            session_db (Session): The database session used to execute queries.
        """

        self.__user_repository = UserRepository(session_db)

    def remove(self, request_path: RemoveUserByUserIdReqPathDTO) -> None:
        """
        Public method responsible for deleting a user.

        This method verifies the user ID, checks if the user exists,
        and removes the user from the database.

        Args:
            user_id (str): The unique identifier of the user to be removed.

        Raises:
            UserNotFoundException: If the user does not exist.
            BaseException: If an unexpected error occurs during deletion.
        """
        try:
            user_id = request_path.user_id

            self.__check_user_id(user_id)

            user = self.__user_repository.find_user(user_id)

            if not user:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            self.__user_repository.remove_user(user)
            self.__user_repository.database.commit()

            log.info(f"User deleted: id: {user_id}, name: {user.name}")

        except BaseException as error:
            log.error(f"Error in DeleteUserUseCase: {error}")
            raise

    def __check_user_id(self, user_id: str) -> None:
        """
        Private method responsible for validating the user ID.

        This method checks if a user ID is provided before attempting deletion.

        Args:
            user_id (str): The user ID to validate.

        Raises:
            UserNotFoundException: If the user ID is missing.
        """

        if not user_id:
            raise UserNotFoundException(
                "User ID is required in the Query Params!"
            )
