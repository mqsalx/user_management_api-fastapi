# /src/presentation/controllers/user/create/__init__.py

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
from src.domain.dtos.request.body.user import CreateUserReqBodyDTO
from src.domain.dtos.response.user import UserResponseDTO
from src.domain.use_cases.user import CreateUserUseCase

# Utils
from src.utils import ResponseUtil

response_json: Callable[..., JSONResponse] = ResponseUtil().json_response


class CreateUserController:
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
        self.__use_case = CreateUserUseCase(self.__repository)

    def __call__(
        self,
        body: CreateUserReqBodyDTO
    ) -> JSONResponse:
        """
        Public method that creates a new user.

        Args:
            request (CreateUserRequestDTO): Data Transfer Object (DTO) containing
                user details required for registration.

        Returns:
            JSONResponse: A JSON response containing the created user's data.
        """

        response = self.__use_case(body)
        message = "User created!"

        return response_json(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )
