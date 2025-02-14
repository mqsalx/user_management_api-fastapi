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
    Class responsible for configuring and providing access to the database connection,
    sessions, and the declarative base for model definitions.
    """

    _db_url = DatabaseConfigurationUtil().get_url()
    _engine = create_engine(_db_url)
    _sessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=_engine
    )
    _base = declarative_base()

    @classmethod
    def get_db(cls) -> Generator[Session, None, None]:
        db = cls._sessionLocal()
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
        cls._base.metadata.create_all(bind=cls._engine)

    @classmethod
    def base(cls) -> Any:
        """
        Class method that returns the declarative base for model definitions.
        Returns:
            Any: The declarative base.
        """
        return cls._base
