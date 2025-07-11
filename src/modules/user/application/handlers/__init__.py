# /src/modules/user/application/handlers/create/__init__.py

# PY
import inspect

from typing import Dict

# Commnands and Queries
from src.modules.user.application.commands import (
    CreateUserCommand,
    RemoveUserCommand,
    UpdateUserCommand
)
from src.modules.user.application.queries import FindUserByUserIdQuery

# Services
from src.modules.user.application.services import UserService

# Entities
from src.modules.user.domain.entities import UserEntity

# Shared
from src.shared.domain.exceptions.base import BaseHTTPException

# Utils
from src.utils import log


class UserHandler:
    """
    Application handler responsible for coordinating user-related use cases.

    This class acts as an interface between incoming commands/queries
        and the service layer,
    handling the orchestration of business operations for user
        creation, retrieval, updating, and removal.
        It also performs logging for exceptions.
    """

    def __init__(self, service: UserService) -> None:
        """
        Initializes the UserHandler with a UserService instance.

        Args:
            service (UserService): Service responsible for user business logic.
        """
        self._service: UserService = service

    async def create_user(self, command: CreateUserCommand) -> Dict[str, str]:
        """
        Handles the use case for creating a new user.

        Args:
            command (CreateUserCommand): The command containing
                user creation data.

        Returns:
            Dict[str, str]: A dictionary with the newly created user's
                basic information.

        Raises:
            BaseHTTPException | Exception: Any error that occurs
                during the operation.
        """
        try:
            created_entity: UserEntity = await self._service.create_user(
                name=command.name,
                email=command.email,
                password=command.password,
                status=command.status,
            )

            return {
                "user_id": str(created_entity.user_id),
                "name": str(created_entity.name),
                "email": str(created_entity.email),
            }

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}")  # noqa: E501
            raise error

    async def find_user_by_user_id(self, query: FindUserByUserIdQuery):
        """
        Handles the use case for retrieving a user by ID.

        Args:
            query (FindUserByUserIdQuery): The query containing the user ID.

        Returns:
            dict: A dictionary with the found user's information.

        Raises:
            BaseHTTPException | Exception: If the user is not found
                or another error occurs.
        """
        try:

            print(query.user_id)
            found_entity: UserEntity = await self._service.find_user_by_id(
                user_id=query.user_id
            )

            return {
                "user_id": found_entity.user_id,
                "name": found_entity.name,
                "email": found_entity.email,
                "status": found_entity.status,
            }

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}")
            raise error

    async def update_user(self, command: UpdateUserCommand):
        """
        Handles the use case for updating an existing user.

        Args:
            command (UpdateUserCommand): The command
                containing the updated user data.

        Returns:
            dict: A dictionary with the updated user information.

        Raises:
            BaseHTTPException | Exception: If the update
                fails or the user does not exist.
        """
        try:
            updated_entity: UserEntity = await self._service.update_user(
                user_id=command.user_id,
                name=command.name,
                email=command.email,
                status=command.status,
            )
            return {
                "user_id": updated_entity.user_id,
                "name": updated_entity.name,
                "email": updated_entity.email,
                "status": updated_entity.status,
            }

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}")
            raise error

    async def remove_user(self, command: RemoveUserCommand):
        """
        Handles the use case for removing a user by ID.

        Args:
            command (RemoveUserCommand): The command containing the user ID to be removed.

        Returns:
            dict: A success message if the user was removed.

        Raises:
            BaseHTTPException | Exception: If the operation fails or the user still exists afterward.
        """
        try:
            await self._service.remove_user(user_id=command.user_id)

            entity: UserEntity | None = await self._service.find_user_by_id(
                user_id=command.user_id
            )

            if not entity:
                return {"message": "User removed successfully"}

            raise

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}")
            raise error
