# /src/core/configurations/database/utils/__init__.py

from typing import LiteralString

# Core
from src.core.configurations.environment import env_config

# Shared
from src.shared.domain.enums import DatabaseTypeEnum


class DatabaseConfigUtil:
    """ """

    def __init__(self) -> None:
        self.__api_name: str = env_config.api_name
        self.__db_type: str = env_config.database_type
        self.__db_name: str = env_config.database_name
        self.__db_host: str = env_config.database_host
        self.__db_port: int = env_config.database_port
        self.__db_user: str = env_config.database_user
        self.__db_password: str = env_config.database_password
        self.__db_type_default: LiteralString = (
            DatabaseTypeEnum.SQLITE.value.upper()
        )

    def get_url(self) -> str:
        """ """
        try:
            checked_type = self.check_database_type(self.__db_type)
            return self.__get_db_config(checked_type)
        except Exception as error:
            print(
                f"[DB Config] Fallback to default (sync) due to error: {error}"
            )
            return self.__get_db_config(self.__db_type_default)

    def get_async_url(self) -> str:
        """ """
        try:
            checked_type = self.check_database_type(self.__db_type)
            return self.__get_async_db_config(checked_type)
        except Exception as error:
            print(
                f"[DB Config] Fallback to default (async) due to error: {error}"  # noqa: E501
            )
            return self.__get_async_db_config(self.__db_type_default)

    def check_database_type(self, db_type: str | None) -> str:
        if (
            db_type is None
            or db_type.upper() not in DatabaseTypeEnum.__members__
        ):
            print(
                "\033[33m\033[1m\n"
                + (
                    f"The DATABASE_TYPE was not loaded from the .env file or is invalid, using {self.__db_type_default} as default!"  # noqa: E501
                )
                + "\033[0m"
            )
            return self.__db_type_default
        return DatabaseTypeEnum[db_type.upper()].value

    def __get_db_config(self, db_type: str) -> str:
        """ """
        _parse_url = f"{self.__db_user}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"  # noqa: E501

        return {
            "PostgreSQL": f"postgresql+psycopg2://{_parse_url}",
            "MySQL": f"mysql+pymysql://{_parse_url}",
            "SQLite": f"sqlite:///{self.__api_name}.db",
        }.get(db_type, f"sqlite:///{self.__api_name}.db")

    def __get_async_db_config(self, db_type: str) -> str:
        """ """
        _parse_url = f"{self.__db_user}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"  # noqa: E501

        return {
            "PostgreSQL": f"postgresql+asyncpg://{_parse_url}",
            "MySQL": f"mysql+aiomysql://{_parse_url}",
            "SQLite": f"sqlite+aiosqlite:///{self.__api_name}.db",
        }.get(db_type, f"sqlite+aiosqlite:///{self.__api_name}.db")


db_config_util = DatabaseConfigUtil()
