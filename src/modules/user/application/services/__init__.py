# /src/modules/user/application/services/create/__init__.py

# Modules
from src.modules.user.domain import IUserRepository
from src.modules.user.domain.entities import UserEntity
from src.modules.user.domain.exceptions import (
    EmailAlreadyExistsException,
    UserNotFoundException,
)

# Shared
from src.shared.domain.unit_of_work import IAsyncUnitOfWork

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
        async_unit_of_work (IAsyncUnitOfWork): Manages
            transactional operations.
    """

    def __init__(
        self,
        repository: IUserRepository,
        async_unit_of_work: IAsyncUnitOfWork,
    ) -> None:
        """
        Initializes the UserService with a user repository and a unit of work.

        Args:
            repository (IUserRepository): Repository for accessing user data.
            async_unit_of_work (AsyncUnitOfWork): Manages
                transactional operations.
        """
        self._repository: IUserRepository = repository
        self._uow: IAsyncUnitOfWork = async_unit_of_work

    async def create_user(
        self, name: str, email: str, password: str, status: str
    ) -> UserEntity:
        """
        Creates a new user after validating that the email
            is not already in use.

        Args:
            name (str): Name of the new user.
            email (str): Email address to register.
            password (str): Plain-text password (to be hashed before storing).
            status (str): Initial status of the user (e.g., "active").

        Returns:
            UserEntity: The newly created user entity.

        Raises:
            EmailAlreadyExistsException: If the email is already registered.
        """
        async with self._uow:
            if await self._repository.find_by_email(email):
                raise EmailAlreadyExistsException(
                    f"User with email {email} already exists!"
                )

            _hashed_password = AuthUtil.generate_password_hash(password)

            new_entity = UserEntity(
                name=name,
                email=email,
                password=_hashed_password,
                status=status,
            )

            created_entity: UserEntity = await self._repository.create(
                entity=new_entity
            )

            await self._uow.commit()

            return created_entity

    async def find_user_by_id(self, user_id: str) -> UserEntity:
        """
        Retrieves a user by their unique ID.

        Args:
            user_id (str): The user's identifier.

        Returns:
            UserEntity: The found user entity.

        Raises:
            UserNotFoundException: If no user is found with the provided ID.
        """
        found_entity: UserEntity | None = await self._repository.find_by_id(
            entity_id=user_id
        )
        if not found_entity:
            print(f"User {user_id} not found.")
            raise UserNotFoundException(message=f"User {user_id} not found.")
        return found_entity

    async def update_user(
        self, user_id: str, name: str, email: str, status: str
    ) -> UserEntity:
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
                await self._repository.find_by_id(entity_id=user_id)
            )
            if not found_entity:
                raise UserNotFoundException(f"User {user_id} not found.")

            updated_entity: UserEntity = await self._repository.update(
                entity=found_entity
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
                await self._repository.find_by_id(entity_id=user_id)
            )

            if not found_entity:
                raise UserNotFoundException(f"User {user_id} not found.")

            await self._repository.remove(entity_id=found_entity.user_id)
            await self._uow.commit()
