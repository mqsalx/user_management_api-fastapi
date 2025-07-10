# /src/modules/user/application/services/create/__init__.py

from src.modules.user.domain import IUserRepository
from src.modules.user.domain.exceptions import (
    EmailAlreadyExistsException,
    UserNotFoundException,
)
from src.modules.user.infrastructure.models import UserModel
from src.modules.user.domain.entities import UserEntity
from src.utils import AuthUtil


class UserService:
    def __init__(self, repository: IUserRepository):
        self._repository: IUserRepository = repository

    async def create_user(
        self, name: str, email: str, password: str, status: str
    ) -> UserModel:
        if await self._repository.find_by_email(email):  # await
            raise EmailAlreadyExistsException(
                f"User with email {email} already exists!"
            )

        hashed_password = AuthUtil.generate_password_hash(password)

        entity = UserEntity(
            name=name,
            email=email,
            password=hashed_password,
            status=status
        )

        return await self._repository.create(entity)

    async def update_user(
        self, user_id: str, name: str, email: str, status: str
    ):
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found.")

        user.name = name
        user.email = email
        user.status = status

        return await self._repository.update(user)

    async def find_user_by_id(self, user_id: str):
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found.")
        return user
