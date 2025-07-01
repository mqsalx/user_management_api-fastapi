# /src/presentation/controllers/user/create/__init__.py

# flake8: noqa: E501

from src.core.configurations.scheduler import scheduler_config
import asyncio

# PY
from typing import Callable
from fastapi import BackgroundTasks, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# Data
from src.data.models import UserModel
from src.data.repositories import UserRepository

# Domain
from src.domain.dtos import (
    CreateUserReqBodyDTO,
    UserResponseDTO
)
from src.domain.use_cases import CreateUserUseCase

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
        self.__repository = UserRepository(session_db)
        self.__use_case = CreateUserUseCase(self.__repository)

    def __call__(
        self,
        body: CreateUserReqBodyDTO,
        background_tasks: BackgroundTasks
    ) -> JSONResponse:
        """
        Public method that creates a new user.

        Args:
            request (CreateUserRequestDTO): Data Transfer Object (DTO) containing
                user details required for registration.

        Returns:
            JSONResponse: A JSON response containing the created user's data.
        """
        use_case_response = self.__use_case(body)

        # background_tasks.add_task(self.__use_case, body)

        # asyncio.create_task(self.__use_case(body))

        # message = "Creating user!"
        message = "User created!"

        # return response_json(
        #     status_code=status.HTTP_202_ACCEPTED,
        #     message=message
        # )
        return response_json(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=UserResponseDTO(root=use_case_response).model_dump(),
        )
