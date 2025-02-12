# /src/utils/database/database_util.py

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from src.core.configurations.env_configuration import EnvConfiguration
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
    DatabaseConfigurationUtil,
)


class DatabaseUtil:

    def __init__(self):

        _db_url = DatabaseConfigurationUtil().create_url()

        self.__database_type = EnvConfiguration().database_type
        self.__engine = create_engine(_db_url)

    def check_connection(self) -> None:

        checked_database_type = (
            DatabaseConfigurationUtil().check_database_type(
                self.__database_type
            )
        )

        try:

            with self.__engine.connect():
                print(
                    f"\033[32m\033[1m\nDatabase -> {checked_database_type} connection successful!\n\033[0m"
                )

        except OperationalError as e:

            print(
                f"\033[31m\033[1m\nDatabase connection failed!\n\033[0m Error: {str(e)}"
            )
            raise

    def setup_database(self):
        DatabaseConfiguration.create_all()
