# /src/modules/user/application/handlers/create/__init__.py

# PY
import inspect
from typing import Dict, List

# Commnands and Queries
from src.modules.user.application.commands import (
    CreateUserCommand,
    RemoveUserCommand,
    UpdateUserCommand,
)
from src.modules.user.application.queries import (
    FindAllUsersQuery,
    FindUserByUserIdQuery,
)

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
                command=command
            )

            formatted_response: Dict[str, str] = self.__response(
                created_entity
            )

            return formatted_response

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"
            )  # noqa: E501
            raise error

    async def find_all_users(self, query: FindAllUsersQuery):
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

            found_entities, pagination = await self._service.find_all_users(
                query
            )

            return self.__response_list(found_entities), pagination

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"
            )
            raise error

    async def find_user_by_user_id(
        self, query: FindUserByUserIdQuery
    ) -> Dict[str, str]:
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

            found_entity: UserEntity = (
                await self._service.find_user_by_user_id(user_id=query.user_id)
            )

            formatted_response: Dict[str, str] = self.__response(found_entity)

            return formatted_response

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"  # noqa: E501
            )
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
                command=command
            )

            formatted_response: Dict[str, str] = self.__response(
                updated_entity
            )

            return formatted_response

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"
            )
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

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"
            )
            raise error

    def __response(self, entity: UserEntity) -> Dict[str, str]:
        """
        Private method responsible for formatting a single user response.

        Args:
            user (UserModel): The user instance to format.

        Returns:
            Dict[str, str]: A dictionary containing user details.
        """

        return {
            "user_id": str(entity.user_id),
            "name": str(entity.name),
            "email": str(entity.email),
            "status": str(entity.status.value),
        }

    def __response_list(
        self, entities: List[UserEntity]
    ) -> List[Dict[str, str]]:
        """
        Private method responsible for formatting a list of users.

        Args:
            entities (List[UserModel]): A list of user instances to format.

        Returns:
            List[Dict[str, str]]: A list of dictionaries
                containing user details.
        """

        return [self.__response(entity=entity) for entity in entities]
