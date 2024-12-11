# /app/repository/user_repository.py

from sqlalchemy.orm import Session

from dtos.user.user_dto import UserCreateDTO
from src.infrastructure.models.user_model import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreateDTO) -> UserModel:
        user = UserModel(
            name=user_data.name, email=user_data.email, status=user_data.status
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_users(self):
        return self.db.query(UserModel).all()
