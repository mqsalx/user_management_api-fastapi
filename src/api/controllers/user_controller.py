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

    def __init__(self, db: Session = Depends(DatabaseConfiguration().get_db)):
        self.__use_case_create = CreateUserUseCase(db).create
        self.__use_case_remove = RemoveUserUseCase(db).remove
        self.__use_case_find = FindUserUseCase(db).find
        self.__use_case_update = UpdateUserUseCase(db).update

    def create_user_controller(
        self, request: CreateUserRequestDTO
    ) -> JSONResponse:

        response = self.__use_case_create(request)

        message = "User created!"

        return response_json(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )

    def remove_user_controller(self, user_id: str) -> JSONResponse:

        self.__use_case_remove(user_id)

        message = "User deleted!"

        return response_json(status_code=status.HTTP_200_OK, message=message)

    def find_user_controller(self, user_id: str | None = None) -> JSONResponse:

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

        response = self.__use_case_update(user_id, request)

        message = "User updated!"

        return ResponseUtil().json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )
