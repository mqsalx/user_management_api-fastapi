# /src/modules/user/presentation/controllers/create/__init__.py

# PY
from typing import Dict

from fastapi.responses import JSONResponse

# Modules
from src.modules.user.application.commands import CreateUserCommand
from src.modules.user.application.handlers import UserHandler
from src.modules.user.application.services import UserService
from src.modules.user.domain.repositories import IUserRepository
from src.modules.user.presentation.schemas.request.body import (
    CreateUserReqBodySchema,
)
from src.modules.user.presentation.schemas.response import UserResponseSchema

# Utils
from src.utils import json_response


class CreateUserController:
    """ """

    def __init__(self, repository: IUserRepository) -> None:
        """ """
        self._handler = UserHandler(service=UserService(repository=repository))

    async def __call__(
        self, request_body: CreateUserReqBodySchema
    ) -> JSONResponse:
        """ """
        command: CreateUserCommand = request_body.to_command()
        user_data: Dict[str, str] = await self._handler.create(command=command)
        user_data = UserResponseSchema(**user_data).model_dump()
        print(f"User created: {user_data}")
        return json_response(
            status_code=201,
            message="User created!",
            data=user_data,
        )
