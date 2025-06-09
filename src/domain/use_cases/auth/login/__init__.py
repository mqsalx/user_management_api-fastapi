# /src/domain/usecases/auth/login/__init__.py

# flake8: noqa: E501

# PY
import uuid

from datetime import datetime
from typing import Dict

# Core
from src.core.exceptions import (
    BaseHTTPException,
    InvalidCredentialsException
)

# Domain
from src.domain.dtos import LoginRequestDTO

# Data
from src.data.models import UserModel
from src.data.repositories import (
    AuthRepository,
    UserRepository
)

# Utils
from src.utils import (
    AuthUtil,
    log
)


class LoginUseCase:
    """
    Class responsible for handling the authentication use case.

    This class manages user authentication by verifying credentials
    and generating JWT tokens.

    Class Args:
        repository (AuthenticationRepository): The repository responsible for querying user data.
    """

    def __init__(
        self,
        auth_repository: AuthRepository,
        user_repository: UserRepository
    ) -> None:
        """
        Constructor method for LoginUseCase.

        Initializes the use case with a repository instance.

        Args:
            repository (AuthenticationRepository): The repository instance for user authentication.
        """

        self.__auth_repository: AuthRepository = auth_repository
        self.__user_repository: UserRepository = user_repository

    def __call__(self, body: LoginRequestDTO):
        """
        Public method responsible for authenticating a user and returning a JWT token.

        This method verifies the user's email and password. If authentication is successful,
        it generates a JWT token containing user details.

        Args:
            body (AuthenticationRequestDTO): The DTO containing the user's email and password.

        Returns:
            Dict[str, str]: A dictionary containing the access token and token type.

        Raises:
            InvalidCredentialsException: If the email or password is incorrect.
            BaseException: If an unexpected error occurs during authentication.
        """

        try:

            user = self.__verify_email(body.email)

            if not user:
                log.info(f"User with email {body.email} not found!")
                raise InvalidCredentialsException("Invalid credentials!")

            password = self.__verify_password(
                body.password, str(user.password)
            )

            if not password:
                log.info(
                    f"Invalid password for user with email {body.email}!"
                )
                raise InvalidCredentialsException("Invalid credentials!")

            active_sessions = self.__auth_repository.find_active_sessions_by_user_id(user.user_id)

            if active_sessions:
                update_data = {
                    "is_active": False,
                    "logout_at": datetime.now(),
                }

                for session in active_sessions:
                    self.__auth_repository.deactivate_session(session, update_data)

            jti = str(uuid.uuid4())

            token_data = self.__prepare_token_data(user, jti)

            access_token = AuthUtil.create_token(token_data)

            self.__auth_repository.create_session(
                user_id=user.user_id,
                jti=jti,
                access_token=access_token,
            )

            return self.__response(access_token)

        except BaseHTTPException as error:
            log.error(f"Error authenticating user: {error}")
            raise

    def __verify_email(self, email: str) -> UserModel | None:
        """
        Private method responsible for checking if an email exists in the database.

        Args:
            email (str): The email address to check.

        Returns:
            UserModel | None: The user instance if found, otherwise None.
        """

        user = self.__user_repository.find_user_by_email(email)

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

    def __response(self, access_token: str) -> Dict[str, str]:
        """
        Private method responsible for formatting the authentication response.

        Args:
            access_token (str): The generated JWT access token.

        Returns:
            Dict[str, str]: A dictionary containing the access token and token type.
        """

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def __prepare_token_data(self, user: UserModel, jti: str):
        """
        Private method responsible for preparing the token data.

        Args:
            user (UserModel): The user instance containing email and role.

        Returns:
            Dict[str, str]: A dictionary containing user email and role.
        """

        return {
            "user_id": str(user.user_id),
            "email": user.email,
            "role": user.role.role_id,
            "jti": jti
        }
