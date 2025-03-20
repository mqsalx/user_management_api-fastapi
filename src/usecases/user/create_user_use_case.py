# /src/usecases/user/create_user_use_case.py

from typing import Dict

from sqlalchemy.orm import Session

from src.core.dtos.user_dto import CreateUserRequestDTO
from src.core.exceptions.base_exception import BaseException
from src.core.exceptions.user_exception import EmailAlreadyExistsException
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.user_repository import UserRepository
from src.utils.any_utils import generate_password_hash
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class CreateUserUseCase:
    """
    Class responsible for handling the user creation use case.

    This class manages the process of creating a new user, transforming the
    DTO into an entity and returning a response DTO.

    Class Args:
        db (Session): The database session required for executing queries.
    """

    def __init__(self, db: Session):
        """
        Constructor method for CreateUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            db (Session): The database session used to execute queries.
        """

        self.__repository = UserRepository(db)

    def create(self, request: CreateUserRequestDTO) -> dict[str, str]:
        """
        Public method responsible for creating a new user.

        This method validates the request, checks if the email is already in use,
        persists the user in the database, and returns a response DTO.

        Args:
            request (CreateUserRequestDTO): The DTO containing user details.

        Returns:
            Dict[str, str]: A dictionary containing the created user's details.

        Raises:
            EmailAlreadyExistsException: If the email is already registered.
            Exception: If an unexpected error occurs during user creation.
        """

        try:

            self.__check_user_email(request.email)

            user = self.__repository.create_user(
                name=request.name,
                email=request.email,
                status=request.status,
                password=generate_password_hash(
                    request.password,
                ),
            )

            return self.__response(user)

        except (Exception, BaseException) as error:
            self.__repository.database.rollback()
            log.error(f"Error during the user creation process: {error}")
            raise error

    def __check_user_email(self, user_email: str) -> None:
        """
        Private method responsible for verifying if the provided email is already registered.

        If the email exists, an `EmailAlreadyExistsException` is raised.

        Args:
            user_email (str): The email address to check.

        Raises:
            EmailAlreadyExistsException: If the email is already registered.
        """

        if self.__repository.find_user_email(user_email):
            raise EmailAlreadyExistsException(
                f"User with email {user_email} already exists!"
            )
        return None

    def __response(self, user: UserModel) -> Dict[str, str]:
        """
        Private method responsible for formatting the user creation response.

        This method structures the user data into a response-friendly format.

        Args:
            user (UserModel): The created user instance.

        Returns:
            Dict[str, str]: A dictionary containing the user ID, name, and email.
        """

        return {
            "user_id": str(user.user_id),
            "name": str(user.name),
            "email": str(user.email),
        }
