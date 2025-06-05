# /src/presentation/controllers/user/__init__.py

# flake8: noqa: E501

# PY
from typing import Callable
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.configurations import DatabaseConfig


# Domain
from src.domain.dtos.request.body.user import CreateUserReqBodyDTO
from src.domain.dtos.request.path.user import (
    RemoveUserByUserIdReqPathDTO,
    UpdateUserReqPathDTO
)
from src.domain.dtos.request.query.user import FindUserByUserIdQueryDTO
from src.domain.dtos.response.user import UserResponseDTO

from src.domain.use_cases.user import (
    CreateUserUseCase,
    FindUserUseCase,
    RemoveUserUseCase,
    UpdateUserUseCase,
)

# Utils
from src.utils import ResponseUtil

response_json: Callable[..., JSONResponse] = ResponseUtil().json_response


class UserController:
    """
    Class Controller responsible for handling user-related requests.

    This class provides endpoints for user creation, retrieval, updating, and deletion.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(self, session_db: Session = Depends(DatabaseConfig().get_db)):
        """
        Constructor method that initializes the UserController with database dependencies.

        Args:
            session_db (Session): The database session used for executing queries.
        """

        self.__use_case_create = CreateUserUseCase(session_db).create
        self.__use_case_remove = RemoveUserUseCase(session_db).remove
        self.__use_case_find = FindUserUseCase(session_db).find
        self.__use_case_update = UpdateUserUseCase(session_db).update

    def create_user_controller(
        self, request_body: CreateUserReqBodyDTO
    ) -> JSONResponse:
        """
        Public method that creates a new user.

        Args:
            request (CreateUserRequestDTO): Data Transfer Object (DTO) containing
                user details required for registration.

        Returns:
            JSONResponse: A JSON response containing the created user's data.
        """

        response = self.__use_case_create(request_body)
        message = "User created!"

        return response_json(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )

    def remove_user_controller(self, request_path: RemoveUserByUserIdReqPathDTO) -> JSONResponse:
        """
        Public method that deletes a user.

        Args:
            user_id (str): Unique identifier of the user to be deleted.

        Returns:
            JSONResponse: A JSON response confirming user deletion.
        """

        self.__use_case_remove(request_path)
        message = "User deleted!"

        return response_json(status_code=status.HTTP_200_OK, message=message)

    def find_user_controller(self, request_query: FindUserByUserIdQueryDTO | None = None) -> JSONResponse:
        """
        Public method that retrieves user(s) based on the provided user ID.

        Args:
            request_query:
                user_id (str, optional): Unique identifier of the user to retrieve.
                    If not provided, retrieves all users.

        Returns:
            JSONResponse: A JSON response containing the requested user data.
        """

        user_id: str | None = request_query.user_id if request_query else None
        response = self.__use_case_find(user_id)

        if isinstance(response, list) and not response:
            return ResponseUtil().json_response(
                status_code=status.HTTP_204_NO_CONTENT
            )

        message = (
            "Users retrieved!"
            if isinstance(response, list)
            else "User retrieved!"
        )

        return ResponseUtil().json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )

    def update_user_controller(
        self, user_id: str, request_path: UpdateUserReqPathDTO
    ) -> JSONResponse:
        """
        Public method that updates an existing user's information.

        Args:
            user_id (str): Unique identifier of the user to be updated.
            request (UpdateUserRequestDTO): Data Transfer Object (DTO) containing
                the updated user information.

        Returns:
            JSONResponse: A JSON response confirming the update and returning updated user data.
        """

        response = self.__use_case_update(user_id, request_path)
        message = "User updated!"

        return ResponseUtil().json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )
