# /src/data/repository/user/__init__.py

# flake8: noqa: E501

# PY
from sqlalchemy.orm import Session

# Data
from src.data.models import TokenModel

# Utils
from src.utils import log


class TokenRepository:
    """
    Class responsible for handling database operations related to user management.

    This repository provides methods for creating, retrieving, and deleting users.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(
        self,
        session_db: Session
    ) -> None:
        """
        Constructor method for UserRepository.

        Initializes the repository with a database session.

        Args:
            session_db (Session): The database session used to execute queries.
        """

        self.__model: TokenModel = TokenModel
        self.__session_db: Session = session_db

    def create_token(self, **kwargs) -> TokenModel:
        """
        Public method responsible for creating a new user in the database.

        This method creates a new `TokenModel` instance, persists it in the database,
        and returns the newly created user.

        Args:
            **kwargs: Arbitrary keyword arguments containing user attributes.

        Returns:
            TokenModel: The newly created user.

        Raises:
            Exception: If an error occurs while inserting the user into the database.
        """

        token = self.__model(**kwargs)

        self.__session_db.add(token)

        self.__session_db.flush()

        self.__session_db.refresh(token)

        return token


    def find_token_by_token_id(self, token_id: str):
        """
        Public method responsible for retrieving a user by their user ID.

        This method queries the database to find a user that is not a super administrator.

        Args:
            token_id (str): The unique identifier of the user.

        Returns:
            TokenModel | None: The user matching the user ID if found, otherwise None.
        """

        return (
            self.__session_db.query(TokenModel)
            .filter(
                self.__model.token_id == token_id
            )
            .first()
        )

    def find_tokens(self) -> list[TokenModel] | None:
        """
        Public method responsible for retrieving all users except super administrators.

        This method queries the database for all users whose role is not `SUPER_ADMINISTRATOR`.

        Args:
            None

        Returns:
            list[TokenModel] | None: A list of users or None if no users are found.
        """

        return (
            self.__session_db.query(TokenModel)
            .all()
        )

    def remove_token(self, user: TokenModel) -> None:
        """
        Public method responsible for removing a user from the database.

        This method deletes a user and commits the change to the database.

        Args:
            user (TokenModel): The user instance to be deleted.

        Raises:
            Exception: If an error occurs while deleting the user.
        """

        self.__session_db.delete(user)

        self.__session_db.commit()
