# /src/presentation/routes/user/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.configurations import DatabaseConfig
from src.presentation.controllers import UserController
from src.domain.dtos import (
    CreateUserRequestDTO,
    UpdateUserRequestDTO
)

user_router = APIRouter()


@user_router.post("", response_model=None)
def create_user_router(
    request: CreateUserRequestDTO,
    session_db: Session = Depends(DatabaseConfig().get_db),
) -> JSONResponse:
    """
    Endpoint that handles user creation.

    This Standalone Function processes user registration requests and returns a confirmation message
    upon successful user creation.

    Args:
        request (CreateUserRequestDTO): Data Transfer Object (DTO) containing the
            user's registration details (e.g., name, email, password).
        session_db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response confirming user creation.

    Raises:
        HTTPException: If user creation fails due to invalid data or database errors.
    """

    controller = UserController(session_db)
    return controller.create_user_controller(request)


@user_router.delete("", response_model=None)
def remove_user_router(
    user_id: str = Query(None, description="User ID to delete."),
    session_db: Session = Depends(DatabaseConfig().get_db),
) -> JSONResponse:
    """
    Endpoint that handles user deletion.

    This Standalone Function removes a user based on the provided user ID.

    Args:
        user_id (str): Unique identifier of the user to delete.
        session_db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response confirming the deletion.

    Raises:
        HTTPException: If the user does not exist or deletion fails.
    """

    controller = UserController(session_db)
    return controller.remove_user_controller(user_id)


@user_router.get("", response_model=None)
def find_user_router(
    user_id: str | None = Query(
        None, description="User ID (optional) to find."
    ),
    session_db: Session = Depends(DatabaseConfig().get_db),
) -> JSONResponse:
    """
    Endpoint that retrieves user(s).

    If a `user_id` is provided, it retrieves a specific user. Otherwise, it returns all users.

    Args:
        user_id (str, optional): Unique identifier of the user to retrieve.
            If not provided, retrieves all users.
        session_db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response containing user details.

    Raises:
        HTTPException: If no users are found.
    """

    controller = UserController(session_db)
    return controller.find_user_controller(user_id)


@user_router.patch("/{user_id}", response_model=None)
def update_user_router(
    user_id: str,
    request: UpdateUserRequestDTO,
    session_db: Session = Depends(DatabaseConfig().get_db),
) -> JSONResponse:
    """
    Endpoint that updates user information.

    This Standalone Function updates the details of an existing user based on the provided user ID.

    Args:
        user_id (str): Unique identifier of the user to update.
        request (UpdateUserRequestDTO): Data Transfer Object (DTO) containing
            the updated user details (e.g., name, email, password).
        session_db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response confirming the update.

    Raises:
        HTTPException: If the user is not found or update fails.
    """

    controller = UserController(session_db)
    return controller.update_user_controller(user_id, request)
