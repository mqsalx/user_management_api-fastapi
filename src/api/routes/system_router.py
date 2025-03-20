# /src/api/routes/system_router.py

from fastapi import APIRouter, Request
from fastapi.routing import APIRoute
from typing import List, Dict

router = APIRouter()


@router.get("/routes", tags=["System"], response_model=None)
def list_routes(request: Request) -> Dict[str, List[Dict[str, str]]]:
    """
    Standalone Function responsible for listing all available API endpoints.

    This function retrieves all registered routes in the FastAPI application, including
    their paths, HTTP methods, and names.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        Dict[str, List[Dict[str, str]]]: A dictionary containing a list of available routes.

        Example:
            {
                "available_routes": [
                    {"path": "/users", "methods": "GET, POST", "name": "get_users"},
                    {"path": "/login", "methods": "POST", "name": "user_login"}
                ]
            }
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
