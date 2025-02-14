# /src/infrastructure/database/database_util.py


from src.core.configurations.env_configuration import EnvConfiguration
from src.core.enums.database_enum import DatabaseTypeEnum


class DatabaseConfigurationUtil:

    def __init__(self):
        self.__api_name = EnvConfiguration().api_name
        self.__db_type = EnvConfiguration().database_type
        self.__db_name = EnvConfiguration().database_name
        self.__db_host = EnvConfiguration().database_host
        self.__db_port = EnvConfiguration().database_port
        self.__db_user = EnvConfiguration().database_user
        self.__db_password = EnvConfiguration().database_password
        self.__db_type_default = DatabaseTypeEnum.SQLITE.value.upper()

    def get_url(self) -> str:
        try:
            _db_type = self.__db_type
            _db_url = None

            checked_database_type = self.check_database_type(_db_type)

            _db_url = self.__get_db_config(checked_database_type)

            return _db_url

        except Exception as error:
            message = (
                f"Error in the process of creating the database url: {error}"
            )
            print(message)
            return self.__get_db_config(self.__db_type_default)

    def check_database_type(self, db_type: str | None) -> str:

        if (
            db_type is None
            or db_type not in DatabaseTypeEnum.__members__.values()
        ):
            print(
                "\033[33m\033[1m\n"
                + f"The DATABASE_TYPE was not loaded from the .env file, using {self.__db_type_default} as default!"
                + "\033[0m"
            )
            return DatabaseTypeEnum[self.__db_type_default].value
        else:
            return DatabaseTypeEnum[db_type.upper()].value

    def __get_db_config(self, db_type: str) -> str:

        _parse_url = f"{self.__db_user}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"

        _db_identifier_config = {
            "PostgreSQL": f"postgresql+psycopg2://{_parse_url}",
            "MySQL": f"mysql+pymysql://{_parse_url}",
            "SQLite": f"sqlite:///{self.__api_name}.db",
        }

        return _db_identifier_config.get(db_type, "SQLite")
