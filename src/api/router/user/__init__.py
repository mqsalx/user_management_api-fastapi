# /src/api/router/user/__init__.py

# PY
from fastapi import APIRouter

# Presentation
from src.modules.user.presentation.routes import CreateUserRouter

user_router = APIRouter()

CreateUserRouter(user_router=user_router)
