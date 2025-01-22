# /src/api/routes/auth/login_router.py

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from src.api.controllers.auth.login_controller import LoginController
from src.core.dtos.auth.login_dto import LoginRequestDTO, LoginResponseDTO

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login/", response_model=LoginResponseDTO)
def login(
    request_data: LoginRequestDTO,
    controller: LoginController,
) -> LoginResponseDTO:
    return controller.login(request_data)
