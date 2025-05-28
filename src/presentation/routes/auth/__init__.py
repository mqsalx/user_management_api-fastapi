# /src/presentation/routes/auth/__init__.py

# flake8: noqa: E501

from typing import Any, Callable, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.presentation.controllers import AuthController
from src.core.configurations import (
    DatabaseConfig,
    EnvConfig
)
from src.domain.dtos import AuthRequestDTO
from src.utils import AuthUtil, ResponseUtil

response_json: Callable[..., JSONResponse] = ResponseUtil().json_response

# Env variables Setup
API_VERSION: str = EnvConfig().api_version

auth_router = APIRouter()


@auth_router.post(path="", response_model=None)
def authorization(
    request: AuthRequestDTO,
    session_db: Session = Depends(DatabaseConfig().get_db),
) -> JSONResponse:
    """
    Endpoint that handles user authentication.

    This standalone function processes login requests by validating the provided credentials
    and returning an authentication token upon successful authentication.

    Args:
        request (AuthRequestDTO): Data Transfer Object (DTO) containing the
            user's login credentials (e.g., email and password).
        session_db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response containing the authentication token if successful.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """

    controller = AuthController(session_db=session_db)
    return controller(request)


@auth_router.get(path="/check", response_model=None)
def check(request: Request) -> JSONResponse | None:
    """
    Endpoint that verifies if the current authentication token is valid.

    This endpoint is protected by the JWT middleware and responds only if
    a valid token is present in the request header.

    Args:
        request (Request): The HTTP request containing the token set by the middleware.

    Returns:
        dict: A dictionary containing a confirmation message and token details.
    """
    token = getattr(request.state, "token", None)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token missing or invalid!"
        )

    payload: Dict[Any, Any] = AuthUtil.verify_token(token=token)

    if payload:
        status_code = status.HTTP_200_OK
        message = "Token is valid!"


        return response_json(
            status_code=status_code,
            message=message,
            data={
                "user": payload.get("user"),
                "role": payload.get("role")
            },
        )

    message = "Invalid token or invalid payload!"

    return response_json(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=message
    )