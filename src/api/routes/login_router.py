# /src/api/routes/login_router.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.controllers.login_controller import LoginController
from src.core.configurations.env_configuration import EnvConfiguration
from src.core.dtos.login_dto import LoginRequestDTO, LoginResponseDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

# Env variables Setup
API_VERSION = EnvConfiguration().api_version

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/api-{API_VERSION}/login",
)


@router.post("", response_model=LoginResponseDTO)
def login(
    request: LoginRequestDTO,
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    """
    Endpoint that handles user authentication.

    This standalone function processes login requests by validating the provided credentials
    and returning an authentication token upon successful authentication.

    Args:
        request (LoginRequestDTO): Data Transfer Object (DTO) containing the
            user's login credentials (e.g., email and password).
        db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response containing the authentication token if successful.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """

    controller = LoginController(db)
    return controller.login(request)
