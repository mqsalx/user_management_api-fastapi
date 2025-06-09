# /src/domain/use_cases/auth/logout/__init__.py

# flake8: noqa: E501

# PY
from datetime import datetime
from fastapi import Request

# Core
from src.core.exceptions import (
    BaseHTTPException,
    UnauthorizedTokenException,
)

# Data
from src.data.repositories import AuthRepository

# Utils
from src.utils import (
    AuthUtil,
    log
)


class LogoutUseCase:
    """
    """
    def __init__(
        self,
        auth_repository: AuthRepository
    ):
        self.__auth_repository: AuthRepository = auth_repository

    def __call__(
        self,
        request: Request
    ):
        """
        """
        try:

            access_token = getattr(request.state, "access_token")

            payload = AuthUtil.verify_token(access_token)

            jwt_id = payload.get("jti")
            if not jwt_id:
                raise UnauthorizedTokenException("Missing JWT ID in token.")

            session = self.__auth_repository.find_session_by_jti(jwt_id)

            if not session or not (session.is_active is True):
                raise UnauthorizedTokenException("Session already inactive or not found.")

            update_data = {
                "is_active": False,
                "logout_at": datetime.now(),
            }
            self.__auth_repository.deactivate_session(session, update_data)

            return {"detail": "Logout successful."}

        except (
            Exception,
            BaseHTTPException
        ) as error:
            log.error(f"Logout failed: {error}")
            raise
