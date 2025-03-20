# /src/api/controllers/login_controller.py

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.dtos.login_dto import LoginRequestDTO, LoginResponseDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.infrastructure.repository.login_repository import LoginRepository
from src.usecases.auth.login_usecase import LoginUseCase
from src.utils.response_util import ResponseUtil

response_json = ResponseUtil().json_response


class LoginController:
    """
    Class Controller responsible for handling user authentication requests.

    This class provides an endpoint to authenticate users, validate credentials,
    and return an access token upon successful authentication.

    Class Args:
        db (Session): The database session used for executing queries.
    """

    def __init__(self, db: Session = Depends(DatabaseConfiguration.get_db)):
        """
        Constructor method that initializes the LoginController with database dependencies.

        Args:
            db (Session): Database session dependency, injected via FastAPI's Depends.
        """
        self.__db = db
        self.__repository = LoginRepository(self.__db)
        self.__usecase = LoginUseCase(self.__repository)

    def login(self, request: LoginRequestDTO) -> JSONResponse:
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
        response = self.__usecase.authenticate_user(request)

        message = "Token generated!"

        return response_json(
            status_code=status.HTTP_200_OK,
            message=message,
            data=LoginResponseDTO(root=response).model_dump(),
        )
