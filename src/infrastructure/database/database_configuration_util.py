# /src/infrastructure/database/database_util.py

from src.core.configurations.env_configuration import EnvConfiguration
from src.core.enums.database_enum import DatabaseTypeEnum
from src.core.exceptions.infrastructure.db_exception import (
    DatabaseInvalidConfigurationException,
)


class DatabaseConfigurationUtil:

    def __init__(self):
        self._db_type = EnvConfiguration().database_type
        self._db_name = EnvConfiguration().database_name
        self._db_host = EnvConfiguration().database_host
        self._db_port = EnvConfiguration().database_port
        self._db_user = EnvConfiguration().database_user
        self._db_password = EnvConfiguration().database_password

        self.__postgresql = DatabaseTypeEnum.POSTGRESQL

    def create_url(self) -> str:
        try:
            _db_type = EnvConfiguration().database_type
            _db_name = EnvConfiguration().database_name
            _db_host = EnvConfiguration().database_host
            _db_port = EnvConfiguration().database_port
            _db_user = EnvConfiguration().database_user
            _db_password = EnvConfiguration().database_password
            _db_url = None

            checked_database_type = self.check_database_type(_db_type)

            if checked_database_type == self.__postgresql:
                _db_identifier = "postgresql+psycopg2"

            _db_url = f"{_db_identifier}://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}"

            return _db_url

        except Exception as error:
            message = (
                f"Error in the process of creating the database url: {error}"
            )
            print(message)
            raise

    def check_database_type(self, db_type) -> str | None:

        if db_type not in DatabaseTypeEnum.__members__.values():
            raise DatabaseInvalidConfigurationException(
                "Invalid database type!"
            )
        else:
            if db_type == self.__postgresql:
                return self.__postgresql.value
