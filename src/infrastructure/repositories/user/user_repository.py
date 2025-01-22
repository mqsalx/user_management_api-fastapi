# /src/adapters/repository/user/user_repository.py

from sqlalchemy.orm import Session

from src.core.entities.user.user_entity import UserEntity
from src.infrastructure.models.user.user_model import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, entity: UserEntity) -> UserModel:
        data = entity.model_dump()
        user = UserModel(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_users(self):
        return self.db.query(UserModel).all()

    def get_email(self, email: str) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.email == email).first()
