# /src/modules/user/presentation/controllers/__init__.py

# PY
from typing import Dict

from fastapi import status
from fastapi.responses import JSONResponse

# Commands
from src.modules.user.application.commands import (
    CreateUserCommand,
    UpdateUserCommand,
    RemoveUserCommand,
)

# Handlers
from src.modules.user.application.handlers import UserHandler

# Queries
from src.modules.user.application.queries import FindUserByUserIdQuery

# Services
from src.modules.user.application.services import UserService

# Repositories
from src.modules.user.domain.repositories import IUserRepository

# Schemas
from src.modules.user.presentation.schemas import (
    CreateUserReqBodySchema,
    FindUserByUserIdQuerySchema,
    UpdateUserReqBodySchema,
    UpdateUserReqPathSchema,
    RemoveUserByUserIdReqPathSchema,
    UserResponseSchema,
)

# Shared
from src.shared.domain.unit_of_work import IAsyncUnitOfWork

# Utils
from src.utils import json_response


class UserController:
    """ """

    def __init__(
        self, repository: IUserRepository, async_unit_of_work: IAsyncUnitOfWork
    ) -> None:
        """ """
        self._handler = UserHandler(
            service=UserService(
                repository=repository, async_unit_of_work=async_unit_of_work
            )
        )

    async def create_user(
        self, request_body: CreateUserReqBodySchema
    ) -> JSONResponse:
        """ """

        command: CreateUserCommand(
            name=request_body.name,
            email=request_body.email,
            password=request_body.password,
            status=request_body.status,
        )

        handler_response: Dict[str, str] = await self._handler.create_user(
            command=command
        )

        controller_response = UserResponseSchema(
            **handler_response
        ).model_dump()

        return json_response(
            status_code=201,
            message="User created!",
            data=controller_response,
        )

    async def find_user(
        self, request_query: FindUserByUserIdQuerySchema
    ) -> JSONResponse:

        # query = FindUserByUserIdQuery(**request_query.model_dump())
        query = FindUserByUserIdQuery(user_id=request_query.user_id)

        handler_response = await self._handler.find_user_by_user_id(
            query=query
        )
        if isinstance(handler_response, list) and not handler_response:
            message = "No users found!"
            return json_response(
                status_code=status.HTTP_200_OK, message=message
            )

        message = (
            "Users retrieved!"
            if isinstance(handler_response, list)
            else "User retrieved!"
        )

        return json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseSchema(root=handler_response).model_dump(),
        )

    async def update_user(
        self,
        request_path: UpdateUserReqPathSchema,
        request_body: UpdateUserReqBodySchema,
    ) -> JSONResponse:
        command: UpdateUserCommand()
        handler_response = await self._handler.update_user(command=command)
        user_data: UserResponseSchema = UserResponseSchema.model_validate(
            handler_response
        )

        return json_response(
            status_code=200,
            message="User updated!",
            data=user_data,
        )

    async def remove_user(self, request_path: RemoveUserByUserIdReqPathSchema) -> JSONResponse:

        command: RemoveUserCommand(user_id=request_path.user_id)

        deleted = await self._handler.remove_user(command=command)


        return json_response(
            status_code=200,
            message="User deleted!",
        )
