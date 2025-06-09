# /src/domain/use_cases/user/remove/__init__.py

# flake8: noqa: E501

# Core
from src.core.exceptions import (
    BaseHTTPException,
    InvalidUserRemovalException,
    UserNotFoundException
)

# Data
from src.data.repositories import UserRepository

# Domain
from src.domain.dtos import RemoveUserByUserIdReqPathDTO

# utils
from src.utils import log


class RemoveUserUseCase:
    """
    Class responsible for handling the user removal use case.

    This class manages the process of deleting a user from the system.

    Class Args:
        session_db (Session): The database session required for executing queries.
    """

    def __init__(
        self,
        repository: UserRepository
    ) -> None:
        """
        Constructor method for RemoveUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            session_db (Session): The database session used to execute queries.
        """

        self.__user_repository: UserRepository = repository

    def __call__(self,
        path: RemoveUserByUserIdReqPathDTO
    ):
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
            user_id = path.user_id

            user = self.__user_repository.find_user(user_id)

            if not user:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            self.__user_repository.remove_user(user)

            user = self.__user_repository.find_user(user_id)

            if user:
                log.info(f"User deleted: id: {user_id}")
                raise InvalidUserRemovalException(
                    f"User with ID {user_id} was not removed successfully!"
                )

        except BaseHTTPException as error:
            log.error(f"Error in DeleteUserUseCase: {error}")
            raise
