# /src/usecases/user/get_user_use_case.py


from typing import Dict, List, Union

from sqlalchemy.orm import Session

from src.core.exceptions.user_exception import UserNotFoundException
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.user_repository import UserRepository
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class FindUserUseCase:
    """
    Class responsible for handling the user search use case.

    This class allows searching for a single user by ID or retrieving all users.

    Class Args:
        db (Session): The database session required for executing queries.
    """

    def __init__(self, db: Session):
        """
        Constructor method for FindUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            db (Session): The database session used to execute queries.
        """
        self.__repository = UserRepository(db)

    def find(
        self, user_id: str | None = None
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
