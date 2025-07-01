# /src/presentation/routes/user/__init__.py

# flake8: noqa: E501

# PY
from fastapi import APIRouter

# Presentation
from src.presentation.routes.user.create import CreateUserRouter
from src.presentation.routes.user.get import GetUserRouter
from src.presentation.routes.user.remove import RemoveUserRouter
from src.presentation.routes.user.update import UpdateUserRouter

user_router = APIRouter()


CreateUserRouter(user_router)
GetUserRouter(user_router)
RemoveUserRouter(user_router)
UpdateUserRouter(user_router)
