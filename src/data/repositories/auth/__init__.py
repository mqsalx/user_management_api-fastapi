# /src/data/repositories/auth/__init__.py

# flake8: noqa: E501

# PY
from sqlalchemy.orm import Session

# Data
from src.data.models import SessionAuthModel

# Utils
from src.utils import log


class AuthRepository:
    """
    Class responsible for handling database operations related to user authentication.

    This repository provides methods for retrieving user data from the database,
    specifically for authentication purposes.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(
        self,
        model: SessionAuthModel,
        session_db: Session
    ):
        """
        Constructor method for AuthRepository.

        Initializes the repository with a database session.

        Args:
            session_db (Session): The database session used to execute queries.
        """

        self.__model: SessionAuthModel = model
        self.__session_db: Session = session_db


    def create_session(self, **kwargs):
        """
        Public method responsible for creating a new user in the database.

        This method creates a new `UserModel` instance, persists it in the database,
        and returns the newly created user.

        Args:
            **kwargs: Arbitrary keyword arguments containing user attributes.

        Returns:
            UserModel: The newly created user.

        Raises:
            Exception: If an error occurs while inserting the user into the database.
        """

        try:

            user = self.__model(**kwargs)

            self.__session_db.add(user)

            self.__session_db.commit()

            self.__session_db.refresh(user)

            return user

        except Exception as error:
            self.__session_db.rollback()
            log.error(f"Error creating session: {error}")
            raise

    def find_session_by_jti(self, jti: str) -> SessionAuthModel | None:
        """
        """
        return self.__session_db.query(SessionAuthModel).filter_by(jti=jti).first()

    def find_active_sessions_by_user_id(self, user_id: str) -> list[SessionAuthModel]:
        """
        """

        return self.__session_db.query(SessionAuthModel).filter_by(
            user_id=user_id,
            is_active=True
        ).all()

    def deactivate_session(self, session: SessionAuthModel, update_data: dict) -> None:
        """
        """
        for field, value in update_data.items():
            if hasattr(session, field):
                setattr(session, field, value)

        self.__session_db.add(session)
        self.__session_db.commit()