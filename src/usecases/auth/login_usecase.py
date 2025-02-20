# /src/usecases/auth/login_usecase.py

from typing import Dict

from src.core.dtos.login_dto import LoginRequestDTO
from src.core.exceptions.login_exception import (
    InvalidCredentialsException,
)
from src.infrastructure.repository.login_repository import LoginRepository
from src.utils.jwt_util import create_token
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class LoginUseCase:
    def __init__(self, login_repository: LoginRepository):
        self.__repository = login_repository

    def authenticate_user(self, request: LoginRequestDTO) -> Dict[str, str]:
        """
        Authenticates a user and returns a JWT token.
        """

        try:

            user = self.__repository.verify_email(request.email)

            if not user:
                raise InvalidCredentialsException("Invalid credentials!")

            password = self.__repository.verify_password(
                request.password, str(user.password)
            )

            if not password:
                raise InvalidCredentialsException("Invalid credentials!")

            token_data = {"sub": user.email}
            token = create_token(token_data)
            return self.__response(token)

        except BaseException as e:
            log.error(f"Error authenticating user: {e}")
            raise

    def __response(self, token: str) -> Dict[str, str]:
        return {
            "access_token": token,
            "token_type": "bearer",
        }
