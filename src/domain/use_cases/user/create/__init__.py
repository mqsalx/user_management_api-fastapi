# /src/domain/use_cases/user/create/__init__.py

# flake8: noqa: E501

# PY
import time
from typing import Dict

# Core
from src.core.exceptions import (
    BaseHTTPException,
    EmailAlreadyExistsException
)

# Data
from src.data.models import UserModel
from src.data.repositories import UserRepository

# Domain
from src.domain.dtos import CreateUserReqBodyDTO

# Utils
from src.utils import (
    AuthUtil,
    log
)


class CreateUserUseCase:
    """
    Class responsible for handling the user creation use case.

    This class manages the process of creating a new user, transforming the
    DTO into an entity and returning a response DTO.

    Class Args:
        repository (UserRepository): The database session required for executing queries.
    """

    def __init__(
        self,
        repository: UserRepository
    ) -> None:
        """
        Constructor method for CreateUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            session_db (Session): The database session used to execute queries.
        """

        self.__repository: UserRepository = repository

    def __call__(
        self,
        body: CreateUserReqBodyDTO
    ):
        """
        Public method responsible for creating a new user.

        This method validates the body, checks if the email is already in use,
        persists the user in the database, and returns a response DTO.

        Args:
            body (CreateUserReqBodyDTO): The DTO containing user details.

        Returns:
            Dict[str, str]: A dictionary containing the created user's details.

        Raises:
            EmailAlreadyExistsException: If the email is already registered.
            Exception: If an unexpected error occurs during user creation.
        """

        try:
            time.sleep(60)
            print("OK")
            print("Creating..")
            self.__check_user_email(body.email)

            user = self.__repository.create_user(
                name=body.name,
                email=body.email,
                status=body.status,
                password=AuthUtil.generate_password_hash(body.password,),
            )

            return self.__response(user)

        except (Exception, BaseHTTPException) as error:
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
