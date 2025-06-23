# /src/presentation/controllers/auth/logout/__init__.py

# PY
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Data
from src.data.models import SessionAuthModel
from src.data.repositories import SessionAuthRepository

# Domain
from src.domain.use_cases import LogoutUseCase


class LogoutController:
    """
    """
    def __init__(
        self,
        session_db: Session
    ):
        """
        """
        self.__session_auth_repository = SessionAuthRepository(
            SessionAuthModel,
            session_db
        )
        self.__use_case = LogoutUseCase(self.__session_auth_repository)

    def __call__(self, request: str) -> JSONResponse:
        """
        """


        use_case_response = self.__use_case(request)


        return JSONResponse(content={"message": "Logout realizado com sucesso"}, status_code=200)
