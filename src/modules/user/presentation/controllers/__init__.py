# /src/modules/user/presentation/controllers/__init__.py

# PY
from fastapi import status
from fastapi.responses import JSONResponse

# Modules
from src.modules.user.application.dtos import (
    CreateUserInput,
    CreateUserOutput,
    FindAllUsersInput,
    FindAllUsersOutput,
    FindUserByUserIdInput,
    FindUserByUserIdOutput,
    RemoveUserInput,
    UpdateUserInput,
    UpdateUserOutput,
)
from src.modules.user.application.use_cases import UserUsecase
from src.modules.user.domain.repositories import IUserRepository
from src.modules.user.domain.services import UserService

# Presentation
from src.modules.user.presentation.schemas import (
    CreateUserReqBodyReq,
    CreateUserResponse,
    FindAllUsersQueryReq,
    FindAllUsersResponse,
    FindUserByUserIdPathReq,
    FindUserByUserIdResponse,
    RemoveUserByUserIdReqPathReq,
    UpdateUserReqBodyReq,
    UpdateUserReqPathReq,
    UpdateUserResponse
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
        self._use_case = UserUsecase(
            async_unit_of_work=async_unit_of_work,
            repository=repository,
            service=UserService(),
        )

    async def create_user(
        self, request_body: CreateUserReqBodyReq
    ) -> JSONResponse:
        """ """

        input = CreateUserInput(
            name=request_body.name,
            email=request_body.email,
            password=request_body.password,
            status=request_body.status,
        )

        handler_response: CreateUserOutput = await self._use_case.create_user(
            input=input
        )

        # controller_response = UserResponseSchema(**handler_response)

        return json_response(
            status_code=201,
            message="User created!",
            data=CreateUserResponse.format(output=handler_response),
        )

    async def find_all_users(
        self, request_query: FindAllUsersQueryReq
    ) -> JSONResponse:

        input = FindAllUsersInput(
            page=request_query.page,
            limit=request_query.limit,
            order=request_query.order,
        )

        handler_response: FindAllUsersOutput = (
            await self._use_case.find_all_users(input=input)
        )

        message = "User retrieved!"

        return json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=FindAllUsersResponse.format(
                output=handler_response.items,
                pagination=handler_response.paginated,
            )
        )

    async def find_user_by_user_id(
        self, request_path: FindUserByUserIdPathReq
    ) -> JSONResponse:

        input = FindUserByUserIdInput(user_id=request_path.user_id)

        handler_response: FindUserByUserIdOutput = (
            await self._use_case.find_user_by_user_id(input=input)
        )

        message = "User retrieved!"

        return json_response(
            status_code=status.HTTP_200_OK,
            message=message,
            data=FindUserByUserIdResponse.format(output=handler_response),
        )

    async def update_user(
        self,
        request_path: UpdateUserReqPathReq,
        request_body: UpdateUserReqBodyReq,
    ) -> JSONResponse:

        input = UpdateUserInput(
            user_id=request_path.user_id,
            name=request_body.name,
            email=request_body.email,
            status=request_body.status,
            password=request_body.password,
        )

        handler_response: UpdateUserOutput = await self._use_case.update_user(
            input=input
        )

        return json_response(
            status_code=200,
            message="User updated!",
            data=UpdateUserResponse.format(output=handler_response)
        )

    async def remove_user(
        self, request_path: RemoveUserByUserIdReqPathReq
    ) -> JSONResponse:

        input = RemoveUserInput(user_id=request_path.user_id)

        await self._use_case.remove_user(input=input)

        return json_response(
            status_code=200,
            message="User deleted!",
        )
