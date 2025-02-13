# /src/usecases/auth/login_usecase.py

from core.dtos.login_dto import LoginRequestDTO, LoginResponseDTO
from core.exceptions.login_exception import (
    InvalidCredentialsException,
)
from src.infrastructure.repository.login_repository import (
    LoginRepository,
)
from utils.jwt_util import create_token
from utils.logger_util import LoggerUtil

log = LoggerUtil()


class LoginUseCase:
    def __init__(self, login_repository: LoginRepository):
        self.__repository = login_repository

    def authenticate_user(self, data: LoginRequestDTO) -> LoginResponseDTO:
        """
        Authenticates a user and returns a JWT token.
        """

        try:

            user = self.__repository.verify_email(data.email)
            if not user or not self.__repository.verify_password(
                data.password
            ):
                raise InvalidCredentialsException("Invalid credentials!")

            # Data for the JWT token
            token_data = {"sub": user.email}
            token = create_token(token_data)
            return token

        except BaseException as e:
            log.error(f"Error authenticating user: {e}")
            raise
