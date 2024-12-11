# /app/controllers/user_controller.py

from fastapi import Depends
from sqlalchemy.orm import Session

from src.adapters.repositories.user_repository import UserRepository
from adapters.validators.user.user_validator import UserValidator
from dtos.user.user_dto import UserCreateDTO
from src.infrastructure.database import get_db
from usecases.user.user_usecase import UserUseCase


class UserController:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = UserRepository(db)
        self.validator = UserValidator(db)
        self.usecase = UserUseCase(self.repository, self.validator)

    def create_user(self, user_data: UserCreateDTO):
        return self.usecase.create_user(user_data)

    def get_user(self, user_id: int):
        return self.usecase.get_user(user_id)

    def get_users(self):
        return self.usecase.get_users()
