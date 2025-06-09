# /src/presentation/controllers/auth/login/__init__.py

# flake8: noqa: E501

# PY
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Data
from src.data.models import (
    SessionAuthModel,
    UserModel
)
from src.data.repositories import (
    AuthRepository,
    UserRepository
)

# Domain
from src.domain.dtos import (
    LoginRequestDTO,
    LoginResponseDTO
)
from src.domain.use_cases import LoginUseCase

# Utils
from src.utils import json_response


class LoginController:
    """
    Class Controller responsible for handling user authentication requests.

    This class provides an endpoint to authenticate users, validate credentials,
    and return an access token upon successful authentication.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(
        self,
        session_db: Session
    ) -> None:
        """
        Constructor method that initializes the LoginController with database dependencies.

        Args:
            session_db (Session): Database session dependency,
                injected via FastAPI's Depends.
        """
        self.__session_db: Session = session_db
        self.__auth_repository = AuthRepository(
            SessionAuthModel,
            self.__session_db
        )
        self.__user_repository = UserRepository(
            UserModel,
            self.__session_db
        )
        self.__use_case = LoginUseCase(
            self.__auth_repository,
            self.__user_repository,
        )

    def __call__(self, body: LoginRequestDTO) -> JSONResponse:
        """
        Public method that authenticates a user based on the provided credentials.

        Args:
            body (AuthenticationRequestDTO): Data Transfer Object (DTO) containing
                the user's login credentials (e.g., email and password).

        Returns:
            JSONResponse: A JSON response containing an authentication token if successful.

        Raises:
            HTTPException: If authentication fails due to invalid credentials.
        """
        response = self.__use_case(body)

        message = "User authenticated successfully!"

        return json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=LoginResponseDTO(root=response).model_dump(),
        )
