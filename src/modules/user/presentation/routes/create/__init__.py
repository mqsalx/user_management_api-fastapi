# /src/presentation/routes/user/create/__init__.py

# PY
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# Modules
from src.modules.user.domain.repositories import IUserRepository
from src.modules.user.presentation.controllers.create import (
    CreateUserController,
)
from src.modules.user.presentation.dependencies import dependencies
from src.modules.user.presentation.schemas.request.body import (
    CreateUserReqBodySchema,
)


class CreateUserRouter:
    """ """
    def __init__(self, user_router: APIRouter) -> None:
        """ """
        self._router: APIRouter = user_router

        self._router.post(
            path="", description="Create a new user", response_model=None
        )(self.__call__)

    async def __call__(
        self,
        request_body: CreateUserReqBodySchema,
        repository: IUserRepository = Depends(
            dependency=dependencies.get_user_repository
        ),
    ) -> JSONResponse:
        """ """
        controller = CreateUserController(repository=repository)
        return await controller(request_body=request_body)
