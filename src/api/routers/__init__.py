# /src/api/router/__init__.py


# PY
from typing import Any, List

from fastapi import APIRouter, Request
from fastapi.routing import APIRoute


class ApiRouter:

    def __init__(self) -> None:
        from src.api.routers.user import UserRouter
        from src.core.configurations import env_config
        self._router = APIRouter()

        self._router.get("", tags=["Api"])(self.__call__)

        routers: List[APIRouter] = [
            UserRouter().router
        ]

        for router in routers:
            self._router.include_router(
                router=router,
                prefix=f"/{env_config.api_version}"
            )

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
        return self._router
