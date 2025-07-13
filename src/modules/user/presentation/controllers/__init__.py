# /src/modules/user/presentation/controllers/__init__.py

# PY
from typing import Dict

from fastapi import status
from fastapi.responses import JSONResponse

# Commands
from src.modules.user.application.commands import (
    CreateUserCommand,
    RemoveUserCommand,
    UpdateUserCommand,
)

# Handlers
from src.modules.user.application.handlers import UserHandler

# Queries
from src.modules.user.application.queries import (
    FindAllUsersQuery,
    FindUserByUserIdQuery,
)

# Services
from src.modules.user.application.services import UserService

# Repositories
from src.modules.user.domain.repositories import IUserRepository

# Schemas
from src.modules.user.presentation.schemas import (
    CreateUserReqBodySchema,
    FindAllUsersQuerySchema,
    FindUserByUserIdPathSchema,
    RemoveUserByUserIdReqPathSchema,
    UpdateUserReqBodySchema,
    UpdateUserReqPathSchema,
    UserResponseSchema,
)
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork

# Utils
from src.utils import json_response


class UserController:
    """ """

    def __init__(
        self, repository: IUserRepository, async_unit_of_work: AsyncUnitOfWork
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

        command = CreateUserCommand(
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

    async def find_all_users(
        self, request_query: FindAllUsersQuerySchema
    ) -> JSONResponse:

        query = FindAllUsersQuery(
            page=request_query.page,
            limit=request_query.limit,
            order=request_query.order,
        )

        entities, pagination = (
            await self._handler.find_all_users(query=query)
        )

        message = "User retrieved!"

        data = {
            "items": [
                UserResponseSchema.model_validate(entity).model_dump()
                for entity in entities
            ],
            **pagination
        }

        return json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=data,
        )

    async def find_user_by_user_id(
        self, request_path: FindUserByUserIdPathSchema
    ) -> JSONResponse:

        query = FindUserByUserIdQuery(user_id=request_path.user_id)

        handler_response: Dict[str, str] = (
            await self._handler.find_user_by_user_id(query=query)
        )

        message = "User retrieved!"

        return json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=UserResponseSchema(**handler_response).model_dump(),
        )

    async def update_user(
        self,
        request_path: UpdateUserReqPathSchema,
        request_body: UpdateUserReqBodySchema,
    ) -> JSONResponse:
        command = UpdateUserCommand(
            user_id=request_path.user_id,
            name=request_body.name,
            email=request_body.email,
            status=request_body.status,
            password=request_body.password,
        )

        handler_response = await self._handler.update_user(command=command)

        user_data: UserResponseSchema = UserResponseSchema.model_validate(
            handler_response
        )

        return json_response(
            status_code=200,
            message="User updated!",
            data=user_data.model_dump(),
        )

    async def remove_user(
        self, request_path: RemoveUserByUserIdReqPathSchema
    ) -> JSONResponse:

        command = RemoveUserCommand(user_id=request_path.user_id)

        await self._handler.remove_user(command=command)

        return json_response(
            status_code=200,
            message="User deleted!",
        )
