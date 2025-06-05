# /src/domain/use_cases/user/find/__init__.py

# flake8: noqa: E501

# PY
from typing import Dict, List, Union

# Core
from src.core.exceptions import UserNotFoundException

# Data
from src.data.models import UserModel
from src.data.repositories import UserRepository

# Domain
from src.domain.dtos.request import FindUserByUserIdQueryDTO

# Utils
from src.utils import log


class FindUserUseCase:
    """
    Class responsible for handling the user search use case.

    This class allows searching for a single user by ID or retrieving all users.

    Class Args:
        db (Session): The database session required for executing queries.
    """

    def __init__(
        self,
        repository: UserRepository
    ):
        """
        Constructor method for FindUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            db (Session): The database session used to execute queries.
        """
        self.__repository: UserRepository = repository

    def __call__(
        self,
        query: FindUserByUserIdQueryDTO
    ) -> Union[Dict[str, str], List[Dict[str, str]]]:
        """
        Public method responsible for searching for a user.

        If a `user_id` is provided, this method searches for the corresponding user.
        If no `user_id` is provided, it retrieves all users.

        Args:
            user_id (str | None, optional): The ID of the user to search for. Defaults to None.

        Returns:
            Union[Dict[str, str], List[Dict[str, str]]]: A dictionary containing user details
            if a single user is found, or a list of dictionaries for multiple users.

        Raises:
            UserNotFoundException: If the specified user ID is invalid.
            Exception: If an unexpected error occurs during user retrieval.
        """

        try:
            user_id = query.user_id
            if user_id is None:
                users = self.__repository.find_users()

                if users is None:
                    log.info("No users found!")
                    return []
                return self.__response_list(users)
            else:
                user = self.__repository.find_user(user_id)
                if not user:
                    raise UserNotFoundException(
                        f"User with ID {user_id} is invalid or incorrect!"
                    )

                return self.__response(user)

        except Exception as error:
            log.error(f"Error in FindUserUseCase: {error}")
            raise

    def __response(self, user: UserModel) -> Dict[str, str]:
        """
        Private method responsible for formatting a single user response.

        Args:
            user (UserModel): The user instance to format.

        Returns:
            Dict[str, str]: A dictionary containing user details.
        """

        return {
            "user_id": str(user.user_id),
            "name": str(user.name),
            "email": str(user.email),
        }

    def __response_list(self, users: List[UserModel]) -> List[Dict[str, str]]:
        """
        Private method responsible for formatting a list of users.

        Args:
            users (List[UserModel]): A list of user instances to format.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing user details.
        """

        return [self.__response(user) for user in users]
