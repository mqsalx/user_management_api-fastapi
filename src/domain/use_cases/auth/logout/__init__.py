# /src/domain/use_cases/auth/logout/__init__.py

# flake8: noqa: E501

# PY
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session

# Core
from src.core.exceptions import (
    BaseHTTPException,
    UnauthorizedTokenException,
)

# Data
from src.data.repositories import SessionAuthRepository

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
        sessio_db: Session
    ):
        self.__session_db = sessio_db

    def __call__(
        self,
        request: Request
    ):
        """
        """
        try:
            with self.__session_db.begin():

                session_auth_repository = SessionAuthRepository(self.__session_db)

                access_token = getattr(request.state, "access_token")

                payload = AuthUtil.verify_token(access_token)

                session_id = payload.get("session_id")

                if not session_id:
                    raise UnauthorizedTokenException("Missing Session ID in token!")

                session = session_auth_repository.find_session_by_session_id(session_id)

                if not session:
                    raise UnauthorizedTokenException("Session already inactive or not found!")

                update_data = {
                    "is_active": False,
                    "logout_at": datetime.now(),
                }

                updated_session = session_auth_repository.deactivate_session(session, update_data)

                session = session_auth_repository.find_active_session_by_session_id(updated_session.session_id)

                if not session:
                    return "Logout successful!"

        except (
            Exception,
            BaseHTTPException
        ) as error:
            log.error(f"Logout failed: {error}")
            raise
