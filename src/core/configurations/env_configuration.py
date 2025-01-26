# /src/core/env/env_variable.py

import os

from dotenv import load_dotenv

load_dotenv()


class EnvConfiguration:

    def __init__(self):

        # API Setup
        self.__api_host: str = str(os.getenv("API_HOST"))
        self.__api_port: int = int(os.getenv("API_PORT"))  # type: ignore
        self.__api_version: str = str(os.getenv("API_VERSION"))

        # Database Setup
        self.__db_url: str = str(os.getenv("DATABASE_URL"))

        # JWT Setup
        self.__jwt_secret_key: str = str(os.getenv("SECRET_KEY"))
        self.__jwt_algorithm: str = str(os.getenv("JWT_ALGORITHM"))
        self.__jwt_access_token_expire_minutes: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")  # type: ignore
        )

    # API Setup
    @property
    def api_host(self) -> str:
        return self.__api_host

    @property
    def api_port(self) -> int:
        return self.__api_port

    @property
    def api_version(self) -> str:
        return self.__api_version

    # Database Setup
    @property
    def db_url(self) -> str:
        return self.__db_url

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
