# /src\presentation\controllers\user\update\__init__.py

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
from src.domain.dtos.request import (
    UpdateUserReqBodyDTO,
    UpdateUserReqPathDTO
)
from src.domain.dtos.response.user import UserResponseDTO
from src.domain.use_cases.user import UpdateUserUseCase

# Utils
from src.utils import ResponseUtil

json_response: Callable[..., JSONResponse] = ResponseUtil().json_response


class UpdateUserController:
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
        self.__use_case = UpdateUserUseCase(self.__repository)

    def __call__(
        self,
        path: UpdateUserReqPathDTO,
        body: UpdateUserReqBodyDTO
    ):
        """
        Public method that deletes a user.

        Args:
            user_id (str): Unique identifier of the user to be deleted.

        Returns:
            JSONResponse: A JSON response confirming user deletion.
        """

        use_case_response = self.__use_case(path, body)
        message = "User updated!"

        return ResponseUtil().json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseDTO(root=use_case_response).model_dump(),
        )
