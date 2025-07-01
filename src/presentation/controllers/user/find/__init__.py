# /src/presentation/controllers/user/find/__init__.py

# flake8: noqa: E501

# PY
from typing import Callable
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Data
from src.data.models import UserModel
from src.data.repositories import UserRepository

# Domain
from src.domain.dtos import (
    FindUserByUserIdQueryDTO,
    UserResponseDTO
)
from src.domain.use_cases import FindUserUseCase

# Utils
from src.utils import ResponseUtil

response_json: Callable[..., JSONResponse] = ResponseUtil().json_response


class FindUserController:
    """
    Class Controller responsible for handling user-related requests.

    This class provides endpoints for user creation, retrieval, updating, and deletion.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(
        self,
        session_db: Session
    ) -> None:
        """
        Constructor method that initializes the UserController with database dependencies.

        Args:
            session_db (Session): The database session used for executing queries.
        """
        self.__repository = UserRepository(
            UserModel,
            session_db,
        )
        self.__use_case = FindUserUseCase(self.__repository)

    def __call__(
        self,
        query: FindUserByUserIdQueryDTO
    ) -> JSONResponse:
        """
        Public method that retrieves user(s) based on the provided user ID.

        Args:
            request_query:
                user_id (str, optional): Unique identifier of the user to retrieve.
                    If not provided, retrieves all users.

        Returns:
            JSONResponse: A JSON response containing the requested user data.
        """

        use_case_response = self.__use_case(query)

        if isinstance(use_case_response, list) and not use_case_response:
            message = "No users found!"
            return ResponseUtil().json_response(
                status_code=status.HTTP_200_OK,
                message=message
            )

        message = (
            "Users retrieved!"
            if isinstance(use_case_response, list)
            else "User retrieved!"
        )

        return ResponseUtil().json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseDTO(root=use_case_response).model_dump(),
        )
