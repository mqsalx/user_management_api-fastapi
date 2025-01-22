# /src/infrastructure/database/__init__.py


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.configurations.env_configuration import EnvConfiguration


class DatabaseConfiguration:

    def __init__(self):
        self.__db_url = EnvConfiguration().db_url

        self.__engine = create_engine(
            self.__db_url, echo=False, pool_pre_ping=True
        )

        self.__session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.__engine
        )

        self.__base = declarative_base()

    @property
    def engine(self):
        return self.__engine

    @property
    def base(self):
        return self.__base

    def get_db(self):
        db = self.__session_local()
        try:
            yield db
        finally:
            db.close()

    def create_all(self):
        self.__base.metadata.create_all(bind=self.__engine)
