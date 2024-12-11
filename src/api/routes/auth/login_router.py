from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.api.controllers.auth.login_controller import LoginController
from src.utils.auth.jwt_utils import verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login/")
def login(email: str, password: str, login_controller: LoginController = Depends(UserController)):
    try:
        return login_controller.login(email, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))