# /src/adapters/repository/user/user_repository.py

from sqlalchemy.orm import Session

from src.infrastructure.models.user.user_model import UserModel


class LoginRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_users(self):
        return self.db.query(UserModel).all()

    def verify_email(self, email: str) -> bool:
        """
        Check if an email already exists in the database.
        """

        user = (
            self.db.query(UserModel).filter(UserModel.email == email).first()
        )

        if user:
            return user
        return False

    def verify_password(self, password: str) -> bool:
        """
        Verify if the provided password matches the stored password for the given email.
        """

        return (
            self.db.query(UserModel)
            .filter(UserModel.password == password)
            .first()
            is not None
        )
