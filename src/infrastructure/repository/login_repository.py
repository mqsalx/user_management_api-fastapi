# /src/adapters/repository/user/user_repository.py

from sqlalchemy.orm import Session

from src.infrastructure.models.user_model import UserModel


class LoginRepository:
    """
    Class responsible for handling database operations related to user authentication.

    This repository provides methods for retrieving user data from the database,
    specifically for authentication purposes.

    Class Args:
        db (Session): The database session used for executing queries.
    """

    def __init__(self, db: Session):
        """
        Constructor method for LoginRepository.

        Initializes the repository with a database session.

        Args:
            db (Session): The database session used to execute queries.
        """

        self.db = db

    def get_user_by_email(self, email: str) -> UserModel | None:
        """
        Public method responsible for retrieving a user by their email.

        This method queries the database to find a user with the specified email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            UserModel | None: The user matching the email if found, otherwise None.
        """

        return (
            self.db.query(UserModel).filter(UserModel.email == email).first()
        )
