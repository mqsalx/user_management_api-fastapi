# /src/adapters/repository/user/user_repository.py

from sqlalchemy.orm import Session

from src.infrastructure.models.user_model import UserModel


class LoginRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> UserModel:
        return (
            self.db.query(UserModel).filter(UserModel.email == email).first()
        )
