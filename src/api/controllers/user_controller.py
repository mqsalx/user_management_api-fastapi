# /src/api/controllers/user_controller.py


from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.dtos.user_dto import (
    CreateUserRequestDTO,
    UpdateUserRequestDTO,
    UserResponseDTO,
)
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.usecases.user.create_user_use_case import CreateUserUseCase
from src.usecases.user.find_user_use_case import FindUserUseCase
from src.usecases.user.remove_user_use_case import RemoveUserUseCase
from src.usecases.user.update_user_use_case import UpdateUserUseCase
from src.utils.response_util import ResponseUtil

response_json = ResponseUtil().json_response


class UserController:
    """
    Class Controller responsible for handling user-related requests.

    This class provides endpoints for user creation, retrieval, updating, and deletion.

    Class Args:
        db (Session): The database session used for executing queries.
    """

    def __init__(self, db: Session = Depends(DatabaseConfiguration().get_db)):
        """
        Constructor method that initializes the UserController with database dependencies.

        Args:
            db (Session): The database session used for executing queries.
        """

        self.__db = db  # The only actual attribute stored in the class

        # Assigning method references from respective use cases
        self.__use_case_create = CreateUserUseCase(db).create
        self.__use_case_remove = RemoveUserUseCase(db).remove
        self.__use_case_find = FindUserUseCase(db).find
        self.__use_case_update = UpdateUserUseCase(db).update

    def create_user_controller(
        self, request: CreateUserRequestDTO
    ) -> JSONResponse:
        """
        Public method that creates a new user.

        Args:
            request (CreateUserRequestDTO): Data Transfer Object (DTO) containing
                user details required for registration.

        Returns:
            JSONResponse: A JSON response containing the created user's data.
        """

        response = self.__use_case_create(request)
        message = "User created!"

        return response_json(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )

    def remove_user_controller(self, user_id: str) -> JSONResponse:
        """
        Public method that deletes a user.

        Args:
            user_id (str): Unique identifier of the user to be deleted.

        Returns:
            JSONResponse: A JSON response confirming user deletion.
        """

        self.__use_case_remove(user_id)
        message = "User deleted!"

        return response_json(status_code=status.HTTP_200_OK, message=message)

    def find_user_controller(self, user_id: str | None = None) -> JSONResponse:
        """
        Public method that retrieves user(s) based on the provided user ID.

        Args:
            user_id (str, optional): Unique identifier of the user to retrieve.
                If not provided, retrieves all users.

        Returns:
            JSONResponse: A JSON response containing the requested user data.
        """

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
        self, user_id: str, request: UpdateUserRequestDTO
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

        response = self.__use_case_update(user_id, request)
        message = "User updated!"

        return ResponseUtil().json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )
