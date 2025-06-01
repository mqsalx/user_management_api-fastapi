# /src/presentation/routes/__init__.py


# PY
from typing import Any, List

from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

# Core
from src.core.configurations.environment import EnvConfig

# Presentation
from src.presentation.routes.auth import auth_router
from src.presentation.routes.user import user_router


class ApiRouter:

    def __init__(self) -> None:

        self.__router = APIRouter()
        self.__api_version: str = EnvConfig().api_version

        routers = [
            (user_router, "/users"),
            (auth_router, "/auth"),
        ]

        for router, prefix in routers:
            self.__router.include_router(
                router=router,
                prefix=f"/{self.__api_version}{prefix}"
            )

        self.__router.get("", tags=["Api"])(self.__call__)

    def __call__(self, request: Request) -> List[Any]:
        """
        Endpoint that lists all available API endpoints.
        """
        app = request.app
        routes = []

        for route in app.routes:
            if isinstance(route, APIRoute):
                methods = ", ".join(route.methods)
                if route.path != "/api":
                    routes.append({
                        "endpoint": route.path,
                        "method": methods,
                        # "description": route.summary,
                    })

        return sorted(routes, key=lambda r: r["endpoint"])

    @property
    def router(self) -> APIRouter:
        return self.__router
