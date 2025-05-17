# /src/data/repository/auth/__init__.py

# flake8: noqa: E501

from sqlalchemy.orm import Session

from src.data.models import UserModel


class AuthRepository:
    """
    Class responsible for handling database operations related to user authentication.

    This repository provides methods for retrieving user data from the database,
    specifically for authentication purposes.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(self, session_db: Session):
        """
        Constructor method for AuthRepository.

        Initializes the repository with a database session.

        Args:
            session_db (Session): The database session used to execute queries.
        """

        self.__session_db = session_db

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
            self.__session_db.query(UserModel).filter(UserModel.email == email).first()
        )
