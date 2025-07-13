# /src/modules/user/presentation/routes/__init__.py

# PY

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# Modules
from src.modules.user.domain.repositories import IUserRepository
from src.modules.user.presentation.controllers import UserController
from src.modules.user.presentation.dependencies import UserDependency
from src.modules.user.presentation.schemas import (
    CreateUserReqBodySchema,
    FindAllUsersQuerySchema,
    FindUserByUserIdPathSchema,
    RemoveUserByUserIdReqPathSchema,
    UpdateUserReqBodySchema,
    UpdateUserReqPathSchema,
)
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork


class UserRouter:
    """
    Router class responsible for handling user-related HTTP endpoints.

    This class registers and manages routes for creating, retrieving,
    updating, and deleting user entities. It delegates business logic
    to the UserController and handles FastAPI dependency injection.

    Class Args:
        router (APIRouter): The FastAPI router to register endpoints on.
        repository (IUserRepository): The user repository
            instance (injected).
        async_unit_of_work (AsyncUnitOfWork): Unit of work for managing
            transactions (injected).
    """

    def __init__(self, router: APIRouter) -> None:
        """
        Initializes the UserRouter with dependencies and registers HTTP routes.

        Args:
            router (APIRouter): The FastAPI router to register endpoints on.
            repository (IUserRepository): The user repository
                instance (injected).
            async_unit_of_work (AsyncUnitOfWork): Unit of work for managing
                transactions (injected).
        """
        self._router: APIRouter = router

        self._router.post(path="")(self.create_user)
        self._router.get(path="")(self.find_all_users)
        self._router.get(path="/{user_id}")(self.find_user_by_user_id)
        self._router.patch(path="/{user_id}")(self.update_user)
        self._router.delete(path="/{user_id}")(self.remove_user)

    async def create_user(
        self,
        request_body: CreateUserReqBodySchema,
        repository: IUserRepository = Depends(
            UserDependency.get_user_repository
        ),
        async_unit_of_work: AsyncUnitOfWork = Depends(
            UserDependency.get_async_unit_of_work
        ),
    ) -> JSONResponse:
        """
        Handles the POST / route for creating a new user.

        Args:
            request_body (CreateUserReqBodySchema): The request payload
                containing user data.

        Returns:
            JSONResponse: A response containing the result of the
                creation operation.
        """
        controller = UserController(
            repository=repository, async_unit_of_work=async_unit_of_work
        )

        return await controller.create_user(request_body=request_body)

    async def find_all_users(
        self,
        request_query: FindAllUsersQuerySchema = Depends(),
        repository: IUserRepository = Depends(
            UserDependency.get_user_repository
        ),
        async_unit_of_work: AsyncUnitOfWork = Depends(
            UserDependency.get_async_unit_of_work
        ),
    ) -> JSONResponse:
        """
        Handles the GET / route to retrieve a user by ID.

        Args:
            request_query (FindAllUsersQuerySchema): The query
                parameters containing filters.

        Returns:
            JSONResponse: A response containing the user data
                or a not-found message.
        """
        controller = UserController(
            repository=repository, async_unit_of_work=async_unit_of_work
        )
        return await controller.find_all_users(request_query=request_query)

    async def find_user_by_user_id(
        self,
        request_path: FindUserByUserIdPathSchema = Depends(),
        repository: IUserRepository = Depends(
            UserDependency.get_user_repository
        ),
        async_unit_of_work: AsyncUnitOfWork = Depends(
            UserDependency.get_async_unit_of_work
        ),
    ) -> JSONResponse:
        """
        Handles the GET / route to retrieve a user by ID.

        Args:
            request_path (FindUserByUserIdQuerySchema): The query
                parameters containing the user ID.

        Returns:
            JSONResponse: A response containing the user data
                or a not-found message.
        """
        controller = UserController(
            repository=repository, async_unit_of_work=async_unit_of_work
        )
        return await controller.find_user_by_user_id(request_path=request_path)

    async def update_user(
        self,
        request_path: UpdateUserReqPathSchema = Depends(
            UpdateUserReqPathSchema.validate_path
        ),
        request_body: UpdateUserReqBodySchema = None,
        repository: IUserRepository = Depends(
            UserDependency.get_user_repository
        ),
        async_unit_of_work: AsyncUnitOfWork = Depends(
            UserDependency.get_async_unit_of_work
        ),
    ) -> JSONResponse:
        """
        Handles the PUT /{user_id} route to update a user's information.

        Args:
            request_path (UpdateUserReqPathSchema): The path parameters
                containing the user ID.
            request_body (UpdateUserReqBodySchema): The request payload
                with updated user data.

        Returns:
            JSONResponse: A response with the updated user information
                or error details.
        """
        controller = UserController(
            repository=repository, async_unit_of_work=async_unit_of_work
        )
        return await controller.update_user(
            request_path=request_path, request_body=request_body
        )

    async def remove_user(
        self,
        request_path: RemoveUserByUserIdReqPathSchema = Depends(),
        repository: IUserRepository = Depends(
            UserDependency.get_user_repository
        ),
        async_unit_of_work: AsyncUnitOfWork = Depends(
            UserDependency.get_async_unit_of_work
        ),
    ) -> JSONResponse:
        """
        Handles the DELETE /{user_id} route to remove a user.

        Args:
            request_path (RemoveUserByUserIdReqPathSchema): The path
                parameters containing the user ID.

        Returns:
            JSONResponse: A response indicating the result
                of the delete operation.
        """
        controller = UserController(
            repository=repository, async_unit_of_work=async_unit_of_work
        )
        return await controller.remove_user(request_path=request_path)
