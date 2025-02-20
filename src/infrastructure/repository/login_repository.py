# /src/adapters/repository/user/user_repository.py

from sqlalchemy.orm import Session

from src.infrastructure.models.user_model import UserModel
from src.utils.any_utils import AnyUtils


class LoginRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> UserModel:
        return (
            self.db.query(UserModel)
            .filter(
                UserModel.user_id == user_id,
            )
            .first()
        )

    def get_users(self):
        return self.db.query(UserModel).all()

    def verify_email(self, email: str) -> UserModel | None:
        """
        Check if an email already exists in the database.
        """

        user = (
            self.db.query(UserModel).filter(UserModel.email == email).first()
        )

        if user:
            return user
        return None

    def verify_password(self, request_password: str, saved_password: str) -> bool:
        """
        Verify if the provided password matches the stored password for the given email.
        """

        return AnyUtils.check_password_hash(request_password, saved_password)
