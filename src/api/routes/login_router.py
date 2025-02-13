# /src/api/routes/login_router.py

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.controllers.login_controller import LoginController
from src.core.configurations.env_configuration import EnvConfiguration
from core.dtos.login_dto import LoginRequestDTO, LoginResponseDTO
from src.infrastructure.database.database_configuration import DatabaseConfiguration

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
) -> LoginResponseDTO:
    controller = LoginController(db)
    return controller.login(request)
