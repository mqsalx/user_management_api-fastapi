# /src/presentation/routes/auth/__init__.py

# flake8: noqa: E501

# PY
from fastapi import APIRouter

# Presentation
from presentation.routes.auth.login import LoginRouter
from src.presentation.routes.auth.logout import LogoutRouter
from src.presentation.routes.auth.validate import ValidateRouter


auth_router = APIRouter()


LoginRouter(auth_router)
LogoutRouter(auth_router)
ValidateRouter(auth_router)
