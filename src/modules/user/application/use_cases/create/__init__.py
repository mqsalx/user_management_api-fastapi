# /src/modules/user/application/services/create/__init__.py

import inspect

from src.modules.user.application.dtos import CreateUserInput, CreateUserOutput
from src.modules.user.domain import IUserRepository
from src.modules.user.domain.entities import UserEntity
from src.modules.user.domain.exceptions import EmailAlreadyExistsException
from src.modules.user.domain.services import UserService
from src.shared.domain.exceptions.base import BaseHTTPException

# Shared
from src.shared.infrastructure.unit_of_work import AsyncUnitOfWork

# Utils
from src.utils import log


class CreateUserUseCase:
    """ """

    def __init__(
        self,
        async_unit_of_work: AsyncUnitOfWork,
        repository: IUserRepository,
        service: UserService
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
        self._service: UserService = service

    async def __call__(self, input: CreateUserInput) -> CreateUserOutput:
        """ """
        try:

            async with self._uow:

                if await self._repository.find_by_email(email=input.email):

                    raise EmailAlreadyExistsException(
                        f"User with email {input.email} already exists!"
                    )

                hashed_password: str = self._service.hash_password(password=input.password)

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
