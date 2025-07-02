# /src/core/env/env_variable.py

# flake8: noqa: E501

import os

from dotenv import load_dotenv

load_dotenv()


class EnvConfig:
    """
    Class responsible for loading environment variables for API, database, and JWT settings.

    This class centralizes environment configurations, ensuring that all required variables
    are retrieved from the system environment and providing structured access through properties.

    Class Args:
        None
    """

    def __init__(self):
        """
        Constructor method that initializes the environment configurations.

        Loads required environment variables and assigns them to class attributes.
        If a variable is not found, a default value may be used where applicable.

        Args:
            None
        """

        # API Setup
        __api_role_permissions: str = str(os.getenv("API_ROLE_PERMISSIONS"))
        __api_user_roles: str = str(os.getenv("API_USER_ROLES"))

        self.__api_name: str = str(
            os.getenv("API_NAME", "user_management_api")
        )
        self.__api_host: str = str(os.getenv("API_HOST", "127.0.0.1"))
        self.__api_port: int = int(os.getenv("API_PORT", 5000))
        self.__api_version: str = str(os.getenv("API_VERSION"))
        self.__api_log_level: str = str(os.getenv("API_LOG_LEVEL", "DEBUG"))
        self.__api_user_administrator: str = str(
            os.getenv("API_USER_ADMINISTRATOR")
        )
        self.__api_password_administrator: str = str(
            os.getenv("API_PASSWORD_ADMINISTRATOR")
        )
        self.__api_role_permissions: list = list(
            [
                permission.strip()
                for permission in __api_role_permissions.split(",")
                if permission.strip()
            ]
        )
        self.__api_user_roles: list = list(
            [
                role.strip()
                for role in __api_user_roles.split(",")
                if role.strip()
            ]
        )

        # Database Setup
        self.__database_type: str = str(os.getenv("DATABASE_TYPE"))
        self.__database_name: str = str(os.getenv("DATABASE_NAME"))
        self.__database_host: str = str(os.getenv("DATABASE_HOST"))
        self.__database_port: int = int(os.getenv("DATABASE_PORT"))  # type: ignore
        self.__database_user: str = str(os.getenv("DATABASE_USER"))
        self.__database_password: str = str(os.getenv("DATABASE_PASSWORD"))

        # JWT Setup
        self.__jwt_secret_key: str = str(os.getenv("SECRET_KEY", "CHANGE-ME"))
        self.__jwt_algorithm: str = str(os.getenv("JWT_ALGORITHM", "HS256"))
        self.__jwt_access_token_expire_minutes: int = int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")  # type: ignore
        )

    # API Setup
    @property
    def api_name(self) -> str:
        """
        Property method responsible for returning the API name.

        Args:
            None

        Returns:
            str: API name.
        """

        return self.__api_name

    @property
    def api_host(self) -> str:
        """
        Property method responsible for returning the API host address.

        Args:
            None

        Returns:
            str: API host.
        """

        return self.__api_host

    @property
    def api_port(self) -> int:
        """
        Property method responsible for returning the API port number.

        Args:
            None

        Returns:
            int: API port.
        """

        return self.__api_port

    @property
    def api_version(self) -> str:
        """
        Property method responsible for returning the API version.

        Args:
            None

        Returns:
            str: API version.
        """

        return self.__api_version

    @property
    def api_log_level(self) -> str:
        """
        Property method responsible for returning the logging level for the API.

        Args:
            None

        Returns:
            str: API log level.
        """

        return self.__api_log_level

    @property
    def api_user_administrator(self) -> str:
        """
        Property method responsible for returning the administrator username.

        Args:
            None

        Returns:
            str: Administrator username.
        """

        return self.__api_user_administrator

    @property
    def api_password_administrator(self) -> str:
        """
        Property method responsible for returning the administrator password.

        Args:
            None

        Returns:
            str: Administrator password.
        """

        return self.__api_password_administrator

    @property
    def api_role_permissions(self) -> list:
        """
        Property method responsible for returning the list of API role permissions.

        Args:
            None

        Returns:
            list: List of API role permissions.
        """

        return self.__api_role_permissions

    @property
    def api_user_roles(self) -> list:
        """
        Property method responsible for returning the list of user roles.

        Args:
            None

        Returns:
            list: List of user roles.
        """

        return self.__api_user_roles

    # Database Setup
    @property
    def database_type(self) -> str:
        """
        Property method responsible for returning the database type.

        Args:
            None

        Returns:
            str: Database type.
        """

        return self.__database_type

    @property
    def database_name(self) -> str:
        """
        Property method responsible for returning the database name.

        Args:
            None

        Returns:
            str: Database name.
        """

        return self.__database_name

    @property
    def database_host(self) -> str:
        """
        Property method responsible for returning the database host address.

        Args:
            None

        Returns:
            str: Database host.
        """

        return self.__database_host

    @property
    def database_port(self) -> int:
        """
        Property method responsible for returning the database port number.

        Args:
            None

        Returns:
            int: Database port.
        """

        return self.__database_port

    @property
    def database_user(self) -> str:
        """
        Property method responsible for returning the database username.

        Args:
            None

        Returns:
            str: Database username.
        """

        return self.__database_user

    @property
    def database_password(self) -> str:
        """
        Property method responsible for returning the database password.

        Args:
            None

        Returns:
            str: Database password.
        """

        return self.__database_password

    # JWT Setup
    @property
    def jwt_secret_key(self) -> str:
        """
        Property method responsible for returning the JWT secret key.

        Args:
            None

        Returns:
            str: JWT secret key.
        """

        return self.__jwt_secret_key

    @property
    def jwt_algorithm(self) -> str:
        """
        Property method responsible for returning the JWT encryption algorithm.

        Args:
            None

        Returns:
            str: JWT encryption algorithm.
        """

        return self.__jwt_algorithm

    @property
    def jwt_access_token_expire_minutes(self) -> int:
        """
        Property method responsible for returning the JWT token expiration time in minutes.

        Args:
            None

        Returns:
            int: JWT token expiration time.
        """

        return self.__jwt_access_token_expire_minutes
