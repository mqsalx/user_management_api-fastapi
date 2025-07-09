# /src/modules/user/application/handlers/create/__init__.py

from typing import Dict
from modules.user.domain.entities import UserEntity
from modules.user.infrastructure.models.user import UserModel
from src.modules.user.application.commands import (
    CreateUserCommand,
    UpdateUserCommand,
)
from src.modules.user.application.queries import FindUserByIdQuery
from src.modules.user.application.services import UserService
from src.core.exceptions import BaseHTTPException
from src.utils import log


class UserHandler:
    def __init__(self, service: UserService):
        self._service: UserService = service

    async def create(self, command: CreateUserCommand) -> Dict[str, str]:
        try:
            entity: UserEntity = await self._service.create_user(
                name=command.name,
                email=command.email,
                password=command.password,
                status=command.status,
            )

            return {
                "user_id": str(object=entity.user_id),
                "name": entity.name,
                "email": entity.email,
            }

        except (Exception, BaseHTTPException) as error:
            log.error(f"Error in CreateUserHandler: {error}")
            raise error

    async def update(self, command: UpdateUserCommand) -> dict:
        user: UserEntity = await self._service.update_user(
            user_id=command.user_id,
            name=command.name,
            email=command.email,
            status=command.status
        )
        return {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "status": user.status
        }

    async def find_by_id(self, query: FindUserByIdQuery) -> dict:
        user: UserEntity = await self._service.find_user_by_id(query.user_id)

        return {
            "user_id": user.use,
            "name": user.name,
            "email": user.email,
            "status": user.status
        }