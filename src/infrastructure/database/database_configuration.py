# /src/infrastructure/database/database_configuration.py

from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.database_configuration_util import (
    DatabaseConfigurationUtil,
)


class DatabaseConfiguration:
    """
    Class responsible for configuring and providing access to the database connection.

    This class initializes the database engine, session factory, and declarative base
    for defining database models. It also provides methods for retrieving database
    sessions and managing table creation.

    Class Args:
        None
    """

    _db_url = DatabaseConfigurationUtil().get_url()
    _engine = create_engine(_db_url)
    _sessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=_engine
    )
    _base = declarative_base()

    @classmethod
    def get_db(cls) -> Generator[Session, None, None]:
        """
        Class method responsible for providing a database session.

        This method creates a new database session, yields it for use,
        and ensures proper cleanup by closing the session afterward.

        Args:
            None

        Yields:
            Generator[Session, None, None]: A database session.

        Raises:
            Exception: If an error occurs while managing the session.
        """

        db = cls._sessionLocal()
        try:
            yield db
        finally:
            db.close()

    @classmethod
    def create_all(cls) -> None:
        """
        Class method responsible for creating all database tables.

        This method initializes the database schema based on the defined models.

        Args:
            None

        Returns:
            None
        """

        cls._base.metadata.create_all(bind=cls._engine)

    @classmethod
    def base(cls) -> Any:
        """
        Class method responsible for returning the declarative base.

        This method provides access to the declarative base used for defining
        database models.

        Args:
            None

        Returns:
            Any: The declarative base instance.
        """

        return cls._base
