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
    Controller for user authentication.
    """

    def __init__(self, db: Session = Depends(DatabaseConfiguration.get_db)):
        self.__db = db
        self.__repository = LoginRepository(self.__db)
        self.__usecase = LoginUseCase(self.__repository)

    def login(
        self,
        request: LoginRequestDTO,
    ) -> JSONResponse:

        response = self.__usecase.authenticate_user(request)

        message = "Token generated!"

        return response_json(
            status_code=status.HTTP_200_OK,
            message=message,
            data=LoginResponseDTO(root=response).model_dump(),
        )
