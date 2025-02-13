# /src/api/controllers/user/user_controller.py


from typing import Optional

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.dtos.user_dto import UserRequestDTO, UserResponseDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.usecases.user.create_user_use_case import CreateUserUseCase
from src.usecases.user.delete_user_use_case import DeleteUserUseCase
from src.usecases.user.get_user_use_case import GetUserUseCase
from src.utils.response_util import ResponseUtil

response_json = ResponseUtil().json_response


class UserController:

    def __init__(self, db: Session = Depends(DatabaseConfiguration().get_db)):
        self.__use_case_create = CreateUserUseCase(db).create
        self.__use_case_delete = DeleteUserUseCase(db).delete
        self.__use_case_get = GetUserUseCase(db).get

    def create_user_handler(self, request: UserRequestDTO) -> JSONResponse:

        response = self.__use_case_create(request)

        message = "User created!"

        return response_json(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=UserResponseDTO(root=response).model_dump(),
        )

    def delete_user_handler(self, user_id: int) -> JSONResponse:

        self.__use_case_delete(user_id)

        message = "User deleted!"

        return response_json(status_code=status.HTTP_200_OK, message=message)

    def get_user_handler(self, user_id: Optional[int] = None) -> JSONResponse:

        response = self.__use_case_get(user_id)

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
