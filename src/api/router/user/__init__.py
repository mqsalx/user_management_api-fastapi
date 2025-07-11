# /src/api/router/user/__init__.py

# PY
from fastapi import APIRouter
from src.modules.user.presentation.routes import UserRouter


user_router = APIRouter()

UserRouter(router=user_router)
