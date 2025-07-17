# /src/api/router/__init__.py


# PY
from typing import Any, List

from fastapi import APIRouter, Request
from fastapi.routing import APIRoute


class ApiRouter:
    """
    Class representing the central API router that aggregates
        and exposes all application routes.

    This class is responsible for:
    - Registering versioned routes (e.g., /v1).
    - Providing a root endpoint (`/api`) that lists all registered endpoints.
    - Dynamically loading and including routers from
        feature modules (e.g., User).
    """
    def __init__(self) -> None:
        """
        Constructor method that initializes the API router.

        This method sets up the main router and includes all versioned routers
        for different application modules (e.g., user).
        """
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
        Method representing the root endpoint (`/api`) that returns
            a list of all available routes.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            List[Any]: A sorted list of dictionaries containing
                endpoint paths and HTTP methods.
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
        """
        Public method that returns the configured FastAPI router.

        Returns:
            APIRouter: The aggregated router with all included routes.
        """
        return self._router
