# src/presentation/interfaces/controllers/auth_controller.py

# PY
from fastapi.responses import JSONResponse

# Presentation
from src.modules.auth.presentation.schemas.request.login import LoginRequest


class ILoginController:
    """
    """

    def __call__(self, body: LoginRequest) -> JSONResponse:
        """
        """
        pass
