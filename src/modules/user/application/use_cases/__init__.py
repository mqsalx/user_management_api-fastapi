# /src/modules/user/application/use_cases/__init__.py

# PY
import inspect
from dataclasses import fields, replace
from math import ceil
from typing import List, NoReturn

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
from src.modules.user.domain.entities import UserEntity
from src.modules.user.domain.exceptions import (
    EmailAlreadyExistsException,
    InvalidUserRemovalException,
    UserNotFoundException,
)
from src.modules.user.domain.repositories import IUserRepository
from src.modules.user.domain.services import UserService

# Shared
from src.shared.domain.exceptions.base import BaseHTTPException
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork

# Utils
from src.utils import log


class UserUsecase:
    """
    Application service responsible for user-related business operations.

    This service coordinates domain logic, repository access, and unit-of-work
    management to perform use cases such as creating, retrieving, updating, and
    removing users.
    """

    def __init__(
        self,
        async_unit_of_work: AsyncUnitOfWork,
        repository: IUserRepository,
        service: UserService,
    ) -> None:
        """
        """
        self._uow: AsyncUnitOfWork = async_unit_of_work
        self._repository: IUserRepository = repository
        self._service: UserService = service

    async def create_user(self, input: CreateUserInput) -> CreateUserOutput:
        """ """
        try:
            async with self._uow:

                if await self._repository.find_by_email(email=input.email):
                    raise EmailAlreadyExistsException(
                        f"User with email {input.email} already exists!"
                    )

                hashed_password: str = self._service.hash_password(
                    password=input.password
                )

                new_entity = UserEntity(
                    name=input.name,
                    email=input.email,
                    password=hashed_password,
                    status=input.status,
                )

                created_entity: UserEntity = await self._repository.create(
                    entity=new_entity
                )

                await self._uow.commit()

                return CreateUserOutput.from_entity(entity=created_entity)

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"  # noqa: E501
            )
            raise error

    async def find_all_users(
        self, input: FindAllUsersInput
    ) -> FindAllUsersOutput:
        """
        """
        try:

            page: int = input.page
            requested_limit: int = input.limit
            order: str = input.order

            total_items: int = await self._repository.find_all(total_count=True)  # type: ignore  # noqa: E501

            min_limit = 1

            max_limit: int = total_items if total_items else 1

            true_limit: int = max(min_limit, min(requested_limit, max_limit))

            offset: int = (page - 1) * true_limit

            found_entities: List[UserEntity] = await self._repository.find_all(
                offset=offset, limit=true_limit, order=order
            )  # type: ignore

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

            return FindAllUsersOutput.format(
                entities=found_entities, pagination=pagination
            )

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"
            )
            raise error

    async def find_user_by_user_id(
        self, input: FindUserByUserIdInput
    ) -> FindUserByUserIdOutput:
        """
        """
        try:

            found_entity: UserEntity | None = (
                await self._repository.find_by_entity_id(
                    entity_id=input.user_id
                )
            )

            if not found_entity:
                raise UserNotFoundException(
                    message=f"User with the ID {input.user_id} not found."
                )

            return FindUserByUserIdOutput.format(entity=found_entity)

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"  # noqa: E501
            )
            raise error

    async def update_user(self, input: UpdateUserInput) -> UpdateUserOutput:
        """
        """
        try:
            async with self._uow:

                found_entity: UserEntity | None = (
                    await self._repository.find_by_entity_id(
                        entity_id=input.user_id
                    )
                )

                if not found_entity:
                    raise UserNotFoundException(
                        f"User {input.user_id} not found."
                    )

                update_fields = {
                    f.name: getattr(input, f.name)
                    for f in fields(input)
                    if "id" not in f.name
                    and getattr(input, f.name) is not None
                }

                to_update_entity: UserEntity = replace(
                    found_entity, **update_fields
                )

                updated_entity: UserEntity = await self._repository.update(
                    entity=to_update_entity
                )

                await self._uow.commit()

                return UpdateUserOutput.format(entity=updated_entity)

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"  # noqa: E501
            )
            raise error

    async def remove_user(self, input: RemoveUserInput) -> None:
        """
        """
        try:
            async with self._uow:

                found_entity: UserEntity | None = (
                    await self._repository.find_by_entity_id(
                        entity_id=input.user_id
                    )
                )

                if not found_entity:
                    raise UserNotFoundException(
                        f"User with the ID {input.user_id} not found."
                    )

                await self._repository.remove(entity_id=found_entity.user_id)

                await self._uow.commit()

                found_entity: UserEntity | None = (
                    await self._repository.find_by_entity_id(
                        entity_id=input.user_id
                    )
                )

                if found_entity:
                    raise InvalidUserRemovalException(
                        f"User {input.user_id} was not removed successfully."
                    )

        except (Exception, BaseHTTPException) as error:
            current_frame = inspect.currentframe()
            caller_frame = inspect.getouterframes(current_frame, 2)[0]
            log.error(
                f"Error in {self.__class__.__name__}.{caller_frame.function}: {error}"
            )
            raise error
