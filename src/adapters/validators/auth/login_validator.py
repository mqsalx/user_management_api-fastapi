# /app/validators/user_validator.py

from sqlalchemy.orm import Session

from src.infrastructure.models.user_model import UserModel


class UserValidator:
    def __init__(self, db: Session):
        self.db = db

    def email_exists(self, email: str) -> bool:
        """Check if an email already exists in the database."""
        return (
            self.db.query(UserModel).filter(UserModel.email == email).first()
            is not None
        )
