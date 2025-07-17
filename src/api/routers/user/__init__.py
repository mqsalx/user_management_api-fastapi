# /src/modules/user/presentation/routes/__init__.py

# PY
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

# Api
from src.api.dependencies.user import UserDependency
from src.api.schemas.user import (
    CreateUserReq,
    FindAllUsersReq,
    FindUserByUserIdReq,
    RemoveUserReq,
    UpdateUserReq,
    UserResponse,
)
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

# Modules
from src.modules.user.application.use_cases import UserUsecase

# Shared


class UserRouter:
    """
    Router class responsible for handling user-related HTTP endpoints.

    This class registers and manages routes for creating, retrieving,
    updating, and deleting user entities. It delegates business logic
    to the UserController and handles FastAPI dependency injection.

    Class Args:
        router (APIRouter): The FastAPI router to register endpoints on.
    """

    def __init__(self) -> None:
        """
        Initializes the UserRouter with dependencies and registers HTTP routes.

        Args:
            router (APIRouter): The FastAPI router to register endpoints on.
        """
        self._router = APIRouter()
        self._router.prefix = "/user"
        self._router.post(path="")(self.create_user)
        self._router.get(path="")(self.find_all_users)
        self._router.get(path="/{user_id}")(self.find_user_by_user_id)
        self._router.patch(path="/{user_id}")(self.update_user)
        self._router.delete(path="/{user_id}")(self.remove_user)

    async def create_user(
        self,
        request: CreateUserReq,
        use_case: UserUsecase = Depends(UserDependency.get_use_case),
    ) -> JSONResponse:
        """
        Method responsible for handling the HTTP POST request
            to create a new user.

        This method receives the request body containing user data,
            maps it to a use case input DTO,
            executes the corresponding use case, and returns a
        standardized HTTP response.

        Args:
            request (CreateUserReq): The request body containing
                the user's name, email, password, and status.
            use_case (UserUsecase): The user use case instance resolved
                via dependency injection.

        Returns:
            JSONResponse: A response object with status 201
                and the created user data.
        """

        input = CreateUserInput(
            name=request.name,
            email=request.email,
            password=request.password,
            status=request.status,
        )

        handler_response: CreateUserOutput = await use_case.create_user(
            input=input
        )

        return UserResponse(
            status_code=201, message="User created", data=handler_response
        )

    async def find_all_users(
        self,
        request: FindAllUsersReq = Depends(FindAllUsersReq),
        use_case: UserUsecase = Depends(UserDependency.get_use_case),
    ) -> JSONResponse:
        """
        Method responsible for handling HTTP GET request
            to retrieve a paginated list of users.

        This method accepts pagination and sorting parameters,
            delegates the processing to the use case,
            and returns a standardized response with pagination metadata.

        Args:
            request (FindAllUsersReq): Query parameters including page,
                limit, and order.
            use_case (UserUsecase): The use case responsible
                for fetching the users.

        Returns:
            JSONResponse: A response with the list of users
                and pagination details.
        """
        input = FindAllUsersInput(
            page=request.page,
            limit=request.limit,
            order=request.order,
        )

        response: FindAllUsersOutput = await use_case.find_all_users(
            input=input
        )

        message = "User retrieved!"

        return UserResponse(
            status_code=200,
            message=message,
            data=response.data,
            pagination=response.pagination,
        )

    async def find_user_by_user_id(
        self,
        request: FindUserByUserIdReq = Depends(FindUserByUserIdReq),
        use_case: UserUsecase = Depends(UserDependency.get_use_case),
    ) -> JSONResponse:
        """
        Method responsible for handling HTTP GET request to retrieve
            a user by their unique identifier.

        This method maps the request to an input DTO, executes the use case,
        and returns the user information if found.

        Args:
            request (FindUserByUserIdReq): Request data containing the user ID.
            use_case (UserUsecase): The use case responsible
                for retrieving the user.

        Returns:
            JSONResponse: A response with the user data or a not-found error.
        """
        input = FindUserByUserIdInput(user_id=request.user_id)

        response: FindUserByUserIdOutput = await use_case.find_user_by_user_id(
            input=input
        )

        message = "User retrieved!"

        return UserResponse(
            status_code=status.HTTP_200_OK,
            message=message,
            data=response,
        )

    async def update_user(
        self,
        request: UpdateUserReq,
        use_case: UserUsecase = Depends(UserDependency.get_use_case),
    ) -> JSONResponse:
        """
        Method responsible for handling the HTTP PUT or PATCH request
            to update an existing user.

        This method receives the updated user data,
            delegates the update logic to the use case,
            and returns the updated user entity in the response.

        Args:
            request (UpdateUserReq): The request body containing
                updated user fields.
            use_case (UserUsecase): The use case responsible for
                processing the update.

        Returns:
            JSONResponse: A response with the updated user data.
        """
        input = UpdateUserInput(
            user_id=request.user_id,
            name=request.name,
            email=request.email,
            status=request.status,
            password=request.password,
        )

        response: UpdateUserOutput = await use_case.update_user(input=input)

        return UserResponse(
            status_code=200,
            message="User updated!",
            data=response,
        )

    async def remove_user(
        self,
        request: RemoveUserReq = Depends(),
        use_case: UserUsecase = Depends(UserDependency.get_use_case),
    ) -> JSONResponse:
        """
        Method responsible for handling the HTTP DELETE request
            to remove a user by ID.

        This method invokes the use case to delete the specified user
        and returns a success message if completed.

        Args:
            request (RemoveUserReq): The request containing the user
                ID to be deleted.
            use_case (UserUsecase): The use case responsible for user removal.

        Returns:
            JSONResponse: A response indicating the user
                was successfully deleted.
        """
        input = RemoveUserInput(user_id=request.user_id)

        await use_case.remove_user(input=input)

        return UserResponse(
            status_code=200,
            message="User deleted!",
        )

    @property
    def router(self) -> APIRouter:
        """
        Public method to retrieve the FastAPI router instance.

        Returns:
            APIRouter: The FastAPI router with registered user routes.
        """
        return self._router
