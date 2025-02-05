# /src/core/env/env_variable.py

import os

from dotenv import load_dotenv

load_dotenv()


class EnvConfiguration:

    def __init__(self):

        # API Setup
        self.__api_name: str = str(os.getenv("API_NAME"))
        self.__api_host: str = str(os.getenv("API_HOST"))
        self.__api_port: int = int(os.getenv("API_PORT"))  # type: ignore
        self.__api_version: str = str(os.getenv("API_VERSION"))
        self.__api_log_level: str = str(os.getenv("API_LOG_LEVEL"))

        # Database Setup
        self.__database_type: str = str(os.getenv("DATABASE_TYPE"))
        self.__database_name: str = str(os.getenv("DATABASE_NAME"))
        self.__database_host: str = str(os.getenv("DATABASE_HOST"))
        self.__database_port: int = int(os.getenv("DATABASE_PORT"))  # type: ignore
        self.__database_user: str = str(os.getenv("DATABASE_USER"))
        self.__database_password: str = str(os.getenv("DATABASE_PASSWORD"))

        # JWT Setup
        self.__jwt_secret_key: str = str(os.getenv("SECRET_KEY"))
        self.__jwt_algorithm: str = str(os.getenv("JWT_ALGORITHM"))
        self.__jwt_access_token_expire_minutes: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")  # type: ignore
        )

    # API Setup
    @property
    def api_name(self) -> str:
        return self.__api_name

    @property
    def api_host(self) -> str:
        return self.__api_host

    @property
    def api_port(self) -> int:
        return self.__api_port

    @property
    def api_version(self) -> str:
        return self.__api_version

    @property
    def api_log_level(self) -> str:
        return self.__api_log_level

    # Database Setup
    @property
    def database_type(self) -> str:
        return self.__database_type

    @property
    def database_name(self) -> str:
        return self.__database_name

    @property
    def database_host(self) -> str:
        return self.__database_host

    @property
    def database_port(self) -> int:
        return self.__database_port

    @property
    def database_user(self) -> str:
        return self.__database_user

    @property
    def database_password(self) -> str:
        return self.__database_password

    # JWT Setup
    @property
    def jwt_secret_key(self) -> str:
        return self.__jwt_secret_key

    @property
    def jwt_algorithm(self) -> str:
        return self.__jwt_algorithm

    @property
    def jwt_access_token_expire_minutes(self) -> int:
        return self.__jwt_access_token_expire_minutes
