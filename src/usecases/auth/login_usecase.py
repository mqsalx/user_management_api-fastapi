# /src/usecases/auth/login_usecase.py

from typing import Dict

from src.core.dtos.login_dto import LoginRequestDTO
from src.core.exceptions.login_exception import InvalidCredentialsException
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.login_repository import LoginRepository
from src.utils.any_utils import AnyUtils
from src.utils.jwt_util import JWTUtil
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
            token = JWTUtil.create_token(token_data)

            return self.__response(token)

        except BaseException as e:
            log.error(f"Error authenticating user: {e}")
            raise

    def __verify_email(self, email: str) -> UserModel | None:
        """
        Check if an email already exists in the database.
        """

        user = self.__repository.get_user_by_email(email)

        if user:
            return user
        return None

    def __verify_password(
        self, request_password: str, saved_password: str
    ) -> bool:
        """
        Verify if the provided password matches the stored password for the given email.
        """

        return AnyUtils.check_password_hash(request_password, saved_password)

    def __response(self, token: str) -> Dict[str, str]:
        return {
            "access_token": token,
            "token_type": "bearer",
        }
