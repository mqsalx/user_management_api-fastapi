# /src/api/controllers/user/user_controller.py


from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.usecases.user.user_usecase_implements import UserUseCaseImplements
from src.utils.response.response_util import ResponseUtil

response_json = ResponseUtil().json_response


class UserController:
    def __init__(self, db: Session = Depends(DatabaseConfiguration().get_db)):
        self.__usecase = UserUseCaseImplements(db)

    def create_user(self, request: UserRequestDTO) -> JSONResponse:

        response = self.__usecase.create_user(request)

        message = "User created"

        return response_json(
            status_code=status.HTTP_201_CREATED,
            message=message,
            data=UserResponseDTO.model_validate(response).model_dump(),
        )

    def get_users(self) -> UserResponseDTO:
        return self.__usecase.get_users()

    def get_user(self, user_id: int) -> UserResponseDTO:
        return self.__usecase.get_user(user_id)
