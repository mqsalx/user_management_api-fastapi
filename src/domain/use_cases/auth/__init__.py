# /src/domain/usecases/auth/__init__.py

# flake8: noqa: E501

from typing import Dict

from src.domain.dtos.auth import AuthRequestDTO
from src.core.exceptions import InvalidCredentialsException
from src.data.models import UserModel
from src.data.repository import AuthRepository
from src.utils import (
    AuthUtil,
    LoggerUtil
)

log = LoggerUtil()


class AuthUseCase:
    """
    Class responsible for handling the authentication use case.

    This class manages user authentication by verifying credentials
    and generating JWT tokens.

    Class Args:
        auth_repository (AuthRepository): The repository responsible for querying user data.
    """

    def __init__(self, auth_repository: AuthRepository):
        """
        Constructor method for LoginUseCase.

        Initializes the use case with a repository instance.

        Args:
            auth_repository (AuthRepository): The repository instance for user authentication.
        """

        self.__repository = auth_repository

    def authenticate_user(self, request: AuthRequestDTO) -> Dict[str, str]:
        """
        Public method responsible for authenticating a user and returning a JWT token.

        This method verifies the user's email and password. If authentication is successful,
        it generates a JWT token containing user details.

        Args:
            request (LoginRequestDTO): The DTO containing the user's email and password.

        Returns:
            Dict[str, str]: A dictionary containing the access token and token type.

        Raises:
            InvalidCredentialsException: If the email or password is incorrect.
            BaseException: If an unexpected error occurs during authentication.
        """

        try:

            user = self.__verify_email(request.email)

            if not user:
                log.info(f"User with email {request.email} not found!")
                raise InvalidCredentialsException("Invalid credentials!")

            password = self.__verify_password(
                request.password, str(user.password)
            )

            if not password:
                log.info(
                    f"Invalid password for user with email {request.email}!"
                )
                raise InvalidCredentialsException("Invalid credentials!")

            token_data = {"user": user.email, "role": user.role.role_id}
            token = AuthUtil.create_token(token_data)

            return self.__response(token)

        except BaseException as e:
            log.error(f"Error authenticating user: {e}")
            raise

    def __verify_email(self, email: str) -> UserModel | None:
        """
        Private method responsible for checking if an email exists in the database.

        Args:
            email (str): The email address to check.

        Returns:
            UserModel | None: The user instance if found, otherwise None.
        """

        user = self.__repository.get_user_by_email(email)

        if user:
            return user
        return None

    def __verify_password(
        self, request_password: str, saved_password: str
    ) -> bool:
        """
        Private method responsible for verifying if the provided password matches the stored password.

        Args:
            request_password (str): The password provided in the login request.
            saved_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the passwords match, otherwise False.
        """

        return AuthUtil.check_password_hash(request_password, saved_password)

    def __response(self, token: str) -> Dict[str, str]:
        """
        Private method responsible for formatting the authentication response.

        Args:
            token (str): The generated JWT access token.

        Returns:
            Dict[str, str]: A dictionary containing the access token and token type.
        """

        return {
            "access_token": token,
            "token_type": "bearer",
        }
