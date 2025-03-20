# /src/api/routes/user_router.py


from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.api.controllers.user_controller import UserController
from src.core.dtos.user_dto import CreateUserRequestDTO, UpdateUserRequestDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)

router = APIRouter()


@router.post("", response_model=None)
def create_user_router(
    request: CreateUserRequestDTO,
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    """
    Endpoint that handles user creation.

    This Standalone Function processes user registration requests and returns a confirmation message
    upon successful user creation.

    Args:
        request (CreateUserRequestDTO): Data Transfer Object (DTO) containing the
            user's registration details (e.g., name, email, password).
        db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response confirming user creation.

    Raises:
        HTTPException: If user creation fails due to invalid data or database errors.
    """

    controller = UserController(db)
    return controller.create_user_controller(request)


@router.delete("", response_model=None)
def remove_user_router(
    user_id: str = Query(None, description="User ID to delete."),
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    """
    Endpoint that handles user deletion.

    This Standalone Function removes a user based on the provided user ID.

    Args:
        user_id (str): Unique identifier of the user to delete.
        db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response confirming the deletion.

    Raises:
        HTTPException: If the user does not exist or deletion fails.
    """

    controller = UserController(db)
    return controller.remove_user_controller(user_id)


@router.get("", response_model=None)
def find_user_router(
    user_id: str | None = Query(
        None, description="User ID (optional) to find."
    ),
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    """
    Endpoint that retrieves user(s).

    If a `user_id` is provided, it retrieves a specific user. Otherwise, it returns all users.

    Args:
        user_id (str, optional): Unique identifier of the user to retrieve.
            If not provided, retrieves all users.
        db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response containing user details.

    Raises:
        HTTPException: If no users are found.
    """

    controller = UserController(db)
    return controller.find_user_controller(user_id)


@router.patch("/{user_id}", response_model=None)
def update_user_router(
    user_id: str,
    request: UpdateUserRequestDTO,
    db: Session = Depends(DatabaseConfiguration().get_db),
) -> JSONResponse:
    """
    Endpoint that updates user information.

    This Standalone Function updates the details of an existing user based on the provided user ID.

    Args:
        user_id (str): Unique identifier of the user to update.
        request (UpdateUserRequestDTO): Data Transfer Object (DTO) containing
            the updated user details (e.g., name, email, password).
        db (Session): Database session dependency, injected via FastAPI's Depends.

    Returns:
        JSONResponse: A JSON response confirming the update.

    Raises:
        HTTPException: If the user is not found or update fails.
    """

    controller = UserController(db)
    return controller.update_user_controller(user_id, request)
