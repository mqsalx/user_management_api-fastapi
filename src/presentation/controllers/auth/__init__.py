# /src/presentation/controllers/auth/__init__.py

# flake8: noqa: E501
from typing import Callable

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.configurations import DatabaseConfig
from src.data.repository import AuthRepository
from src.domain.dtos import AuthRequestDTO, AuthResponseDTO
from src.domain.use_cases.auth import AuthUseCase
from src.utils import ResponseUtil

response_json: Callable[..., JSONResponse] = ResponseUtil().json_response


class AuthController:
    """
    Class Controller responsible for handling user authentication requests.

    This class provides an endpoint to authenticate users, validate credentials,
    and return an access token upon successful authentication.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(
        self, session_db: Session = Depends(DatabaseConfig.get_db)
    ) -> None:
        """
        Constructor method that initializes the LoginController with database dependencies.

        Args:
            session_db (Session): Database session dependency, injected via FastAPI's Depends.
        """
        self.__session_db: Session = session_db
        self.__auth_repository = AuthRepository(session_db=self.__session_db)
        self.__auth_use_case = AuthUseCase(
            auth_repository=self.__auth_repository
        )

    def __call__(self, request: AuthRequestDTO) -> JSONResponse:
        """
        Public method that authenticates a user based on the provided credentials.

        Args:
            request (LoginRequestDTO): Data Transfer Object (DTO) containing
                the user's login credentials (e.g., email and password).

        Returns:
            JSONResponse: A JSON response containing an authentication token if successful.

        Raises:
            HTTPException: If authentication fails due to invalid credentials.
        """
        response = self.__auth_use_case.authenticate_user(request)

        message = "Token generated!"

        return response_json(
            status_code=status.HTTP_200_OK,
            message=message,
            data=AuthResponseDTO(root=response).model_dump(),
        )
