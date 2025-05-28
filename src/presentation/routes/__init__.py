# /src/presentation/routes/__init__.py

# flake8: noqa: E501, F401

from typing import Dict, List

from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

from src.presentation.routes.auth import auth_router
from src.presentation.routes.user import user_router


api_router = APIRouter()


@api_router.get("/routes", tags=["System"], response_model=None)
def list_routes(request: Request) -> Dict[str, List[Dict[str, str]]]:
    """
    Standalone Function responsible for listing all available API endpoints.

    This function retrieves all registered routes in the FastAPI application, including
    their paths, HTTP methods, and names.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        Dict[str, List[Dict[str, str]]]: A dictionary containing a list of available routes.
    """
    app = request.app
    routes = []

    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ", ".join(route.methods)
            routes.append(
                {"path": route.path, "methods": methods, "name": route.name}
            )

    return {"available_routes": routes}
