# /src/presentation/routes/auth/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.presentation.controllers import AuthController
from src.core.configurations import (
    DatabaseConfig,
    EnvConfig
)
from src.domain.dtos import AuthRequestDTO

# Env variables Setup
API_VERSION = EnvConfig().api_version

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/api-{API_VERSION}/login",
)


@auth_router.post("", response_model=None)
def login(
    request: AuthRequestDTO,
    session_db: Session = Depends(DatabaseConfig().get_db),
) -> JSONResponse:
    """
    Endpoint that handles user authentication.

    This standalone function processes login requests by validating the provided credentials
    and returning an authentication token upon successful authentication.

    Args:
        request (AuthRequestDTO): Data Transfer Object (DTO) containing the
            user's login credentials (e.g., email and password).
        session_db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response containing the authentication token if successful.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """

    controller = AuthController(session_db)
    return controller.login(request)
