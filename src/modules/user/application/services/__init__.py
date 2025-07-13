# /src/modules/user/application/services/create/__init__.py

# PY
from dataclasses import fields, replace
from math import ceil

# Modules
from src.modules.user.application.commands import (
    CreateUserCommand,
    UpdateUserCommand,
)

# Queries
from src.modules.user.application.queries import FindAllUsersQuery
from src.modules.user.domain import IUserRepository
from src.modules.user.domain.entities import UserEntity
from src.modules.user.domain.exceptions import (
    EmailAlreadyExistsException,
    InvalidUserRemovalException,
    UserNotFoundException,
)

# Shared
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork

# Utils
from src.utils import AuthUtil


class UserService:
    """
    Application service responsible for user-related business operations.

    This service coordinates domain logic, repository access, and unit-of-work
    management to perform use cases such as creating, retrieving, updating, and
    removing users.

    Class Args:
        repository (IUserRepository): Repository for accessing user data.
        async_unit_of_work (AsyncUnitOfWork): Manages
            transactional operations.
    """

    def __init__(
        self,
        repository: IUserRepository,
        async_unit_of_work: AsyncUnitOfWork,
    ) -> None:
        """
        Initializes the UserService with a user repository and a unit of work.

        Args:
            repository (IUserRepository): Repository for accessing user data.
            async_unit_of_work (AsyncUnitOfWork): Manages
                transactional operations.
        """
        self._repository: IUserRepository = repository
        self._uow: AsyncUnitOfWork = async_unit_of_work

    async def create_user(self, command: CreateUserCommand) -> UserEntity:
        """
        Creates a new user after validating that the email
            is not already in use.

        Args:
            command (CreateUserCommand): Name of the new user.

        Returns:
            UserEntity: The newly created user entity.

        Raises:
            EmailAlreadyExistsException: If the email is already registered.
        """
        async with self._uow:
            if await self._repository.find_by_email(email=command.email):
                raise EmailAlreadyExistsException(
                    f"User with email {command.email} already exists!"
                )

            _hashed_password = AuthUtil.generate_password_hash(
                password=command.password
            )

            new_entity = UserEntity(
                name=command.name,
                email=command.email,
                password=_hashed_password,
                status=command.status,
            )

            created_entity: UserEntity = await self._repository.create(
                entity=new_entity
            )

            await self._uow.commit()

            return created_entity

    async def find_all_users(self, query: FindAllUsersQuery) -> UserEntity:
        """
        Retrieves a user by their unique ID.

        Args:
            user_id (str): The user's identifier.

        Returns:
            UserEntity: The found user entity.

        Raises:
            UserNotFoundException: If no user is found with the provided ID.
        """

        page: int = query.page
        requested_limit: int = query.limit
        order: str = query.order

        total_items = await self._repository.find_all(total_count=True)

        min_limit = 1

        max_limit = total_items if total_items else 1

        true_limit: int = max(min_limit, min(requested_limit, max_limit))

        offset = (page - 1) * true_limit

        found_entities = await self._repository.find_all(
            offset=offset, limit=true_limit, order=order
        )

        if not found_entities:
            raise UserNotFoundException(message="Users not found.")

        total_pages = ceil(total_items / true_limit)

        pagination = {
            "page": page,
            "limit": true_limit,
            "order": order,
            "actual_limit": true_limit,
            "max_limit": max_limit,
            "total_items": total_items,
            "total_pages": total_pages,
        }

        return found_entities, pagination

    async def find_user_by_user_id(self, user_id: str) -> UserEntity:
        """
        Retrieves a user by their unique ID.

        Args:
            user_id (str): The user's identifier.

        Returns:
            UserEntity: The found user entity.

        Raises:
            UserNotFoundException: If no user is found with the provided ID.
        """
        found_entity: UserEntity | None = (
            await self._repository.find_by_entity_id(entity_id=user_id)
        )

        if not found_entity:
            raise UserNotFoundException(
                message=f"User with the ID {user_id} not found."
            )
        return found_entity

    async def update_user(self, command: UpdateUserCommand) -> UserEntity:
        """
        Updates an existing user's information.

        Args:
            user_id (str): The ID of the user to update.
            name (str): The new name.
            email (str): The new email.
            status (str): The new status (e.g., "active").

        Returns:
            UserEntity: The updated user entity.

        Raises:
            UserNotFoundException: If the user does not exist.
        """
        async with self._uow:

            found_entity: UserEntity | None = (
                await self._repository.find_by_entity_id(
                    entity_id=command.user_id
                )
            )

            if not found_entity:
                raise UserNotFoundException(
                    f"User {command.user_id} not found."
                )

            update_fields = {
                f.name: getattr(command, f.name)
                for f in fields(command)
                if "id" not in f.name and getattr(command, f.name) is not None
            }

            to_update_entity: UserEntity = replace(
                found_entity, **update_fields
            )

            updated_entity: UserEntity = await self._repository.update(
                entity=to_update_entity
            )

            await self._uow.commit()

            return updated_entity

    async def remove_user(self, user_id: str) -> None:
        """
        Removes a user from the system by ID.

        Args:
            user_id (str): The ID of the user to be removed.

        Raises:
            UserNotFoundException: If the user does not exist.
        """
        async with self._uow:

            found_entity: UserEntity | None = (
                await self._repository.find_by_entity_id(entity_id=user_id)
            )

            if not found_entity:
                raise UserNotFoundException(
                    f"User with the ID {user_id} not found."
                )

            await self._repository.remove(entity_id=found_entity.user_id)

            await self._uow.commit()

            found_entity: UserEntity | None = (
                await self._repository.find_by_entity_id(entity_id=user_id)
            )

            if found_entity:
                raise InvalidUserRemovalException(
                    f"User {user_id} was not removed successfully."
                )
