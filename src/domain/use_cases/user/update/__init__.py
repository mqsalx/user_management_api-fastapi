# /src/domain/use_cases/user/update/__init__.py

# flake8: noqa: E501

# PY
from typing import Dict

# Core
from src.core.exceptions import (
    BaseHTTPException,
    UserNotFoundException
)

# Data
from src.data.models import UserModel
from src.data.repositories import UserRepository

# Domain
from src.domain.dtos import (
    UpdateUserReqBodyDTO,
    UpdateUserReqPathDTO
)

from src.utils import log


class UpdateUserUseCase:
    """
    Class responsible for handling the user update use case.

    This class updates an existing user with only the provided fields.

    Class Args:
        session_db (Session): The database session required for executing queries.
    """

    def __init__(self, repository: UserRepository) -> None:
        """
        Constructor method for UpdateUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            session_db (Session): The database session used to execute queries.
        """

        self.__user_repository: UserRepository = repository

    def __call__(
        self,
        path: UpdateUserReqPathDTO,
        body: UpdateUserReqBodyDTO
    ) -> dict[str, str]:
        """
        Public method responsible for updating a user.

        This method updates only the fields provided in the request DTO.
        If the user ID is invalid or does not exist, an exception is raised.

        Args:
            user_id (str): The unique identifier of the user to update.
            request (UpdateUserRequestDTO): The DTO containing the fields to update.

        Returns:
            Dict[str, str]: A dictionary containing the updated user details.

        Raises:
            UserNotFoundException: If the user ID is invalid or not found.
            Exception: If an unexpected error occurs during the update process.
        """

        try:
            user_id = path.user_id

            if not user_id:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            user = self.__user_repository.find_user(user_id)

            if not user:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            update_data = body.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)

            self.__user_repository.database.commit()
            self.__user_repository.database.refresh(user)

            return self.__response(user)

        except (
            Exception,
            BaseHTTPException
        ) as error:
            self.__user_repository.database.rollback()
            log.error(f"Error during the user update process: {error}")
            raise error

    def __response(self, user: UserModel) -> Dict[str, str]:
        """
        Private method responsible for formatting the updated user response.

        Args:
            user (UserModel): The updated user instance.

        Returns:
            Dict[str, str]: A dictionary containing the user ID, name, and email.
        """

        return {
            "user_id": str(user.user_id),
            "name": str(user.name),
            "email": str(user.email),
        }
