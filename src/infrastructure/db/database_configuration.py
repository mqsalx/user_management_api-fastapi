# /src/infrastructure/database/__init__.py

from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.core.configurations.env_configuration import EnvConfiguration


class DatabaseConfiguration:
    """
    Class responsible for configuring and providing access to the database connection,
    sessions, and the declarative base for model definitions.
    """

    __db_url = EnvConfiguration().db_url
    __engine = create_engine(
        __db_url, connect_args={"check_same_thread": False}
    )
    __sessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=__engine
    )
    __base = declarative_base()

    @classmethod
    def get_db(cls) -> Generator[Session, None, None]:
        """
        Class method that provides a database session.

        Yields:
            Session: A database session.

        The session is automatically closed after use.
        """

        db = cls.__sessionLocal()
        try:
            yield db
        finally:
            db.close()

    @classmethod
    def create_all(cls) -> None:
        """
        Class method that creates all database tables based on the defined models.

        Returns:
            None
        """

        cls.__base.metadata.create_all(bind=cls.__engine)

    @classmethod
    def base(cls) -> Any:
        """
        Class method that returns the declarative base for model definitions.

        Returns:
            Any: The declarative base.
        """

        return cls.__base
