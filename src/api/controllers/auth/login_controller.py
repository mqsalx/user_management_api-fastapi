# /src/api/controllers/auth/login_controller.py

from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.db.database_configuration import DatabaseConfiguration
from src.core.dtos.auth.login_dto import LoginRequestDTO, LoginResponseDTO
from src.infrastructure.repositories.auth.login_repository import LoginRepository
from src.usecases.auth.login_usecase import LoginUseCase


class LoginController:
    """
    Controller for user authentication.
    """

    def __init__(self, db: Session = Depends(DatabaseConfiguration().get_db)):
        self.__repository = LoginRepository(db)
        self.__usecase = LoginUseCase(self.__repository)

    def login(self, data: LoginRequestDTO) -> LoginResponseDTO:
        token = self.__usecase.authenticate_user(data)
        return LoginResponseDTO(access_token=token, token_type="bearer")
