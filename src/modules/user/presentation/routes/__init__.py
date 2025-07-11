# /src/modules/user/presentation/routes/__init__.py

# PY
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

# Modules
from src.modules.user.presentation.dependencies import dependencies
from src.modules.user.presentation.controllers import UserController
from src.modules.user.presentation.schemas import (
    CreateUserReqBodySchema,
    FindUserByUserIdQuerySchema,
    RemoveUserByUserIdReqPathSchema,
    UpdateUserReqBodySchema,
    UpdateUserReqPathSchema,
)


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

    def __init__(
        self,
        router: APIRouter
    ) -> None:
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

        self._controller = UserController(
            repository=Depends(dependencies.get_user_repository),
            async_unit_of_work=Depends(dependencies.get_user_unit_of_work),

        )

        self._router.post("")(self.create_user)
        self._router.get("")(self.find_user)
        self._router.put("/{user_id}")(self.update_user)
        self._router.delete("/{user_id}")(self.remove_user)

    async def create_user(
        self,
        request_body: CreateUserReqBodySchema,
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
        return await self._controller.create_user(request_body=request_body)

    async def find_user(
        self,
        request_query: FindUserByUserIdQuerySchema = Depends(),
    ) -> JSONResponse:
        """
        Handles the GET / route to retrieve a user by ID.

        Args:
            request_query (FindUserByUserIdQuerySchema): The query
                parameters containing the user ID.

        Returns:
            JSONResponse: A response containing the user data
                or a not-found message.
        """
        return await self._controller.find_user(
            request_query=request_query
        )

    async def remove_user(
        self,
        request_path: RemoveUserByUserIdReqPathSchema = Depends(),
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
        return await self._controller.remove_user(request_path=request_path)

    async def update_user(
        self,
        request_path: UpdateUserReqPathSchema = Depends(
            UpdateUserReqPathSchema.validate_path
        ),
        request_body: UpdateUserReqBodySchema = None,
    ) -> JSONResponse:
        """
        Handles the PUT /{user_id} route to update a user's information.

        Args:
            request_path (UpdateUserReqPathSchema): The path parameters
                containing the user ID.
            request_body (UpdateUserReqBodySchema): The request payload
                with updated user data.

        Returns:
            JSONResponse: A response with the updated user information or error details.
        """
        return await self._controller.update_user(
            request_path=request_path, request_body=request_body
        )
