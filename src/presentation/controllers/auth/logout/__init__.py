# /src/presentation/controllers/auth/logout/__init__.py

# PY
from typing import Literal
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Domain
from src.domain.use_cases import LogoutUseCase

# Utils
from src.utils import json_response

class LogoutController:
    """
    """
    def __init__(
        self,
        session_db: Session
    ):
        """
        """
        self.__use_case = LogoutUseCase(session_db)

    def __call__(self, request: str) -> JSONResponse:
        """
        """

        use_case_response: Literal['Logout successful!'] = self.__use_case(request)

        status_code = status.HTTP_400_BAD_REQUEST
        message = use_case_response

        if use_case_response:
            status_code = status.HTTP_200_OK
            message = use_case_response

        return json_response(
            status_code=status_code,
            message=message
        )