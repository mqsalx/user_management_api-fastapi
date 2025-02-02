# /src/infrastructure/database/postgresql/postgresql_client.py

import psycopg2
from psycopg2 import OperationalError

from src.core.configurations.env_configuration import EnvConfiguration


class PostgreSQLClient:

    def __init__(self):
        self.__host = EnvConfiguration().postgresql_host
        self.__port = EnvConfiguration().postgresql_port
        self.__user = EnvConfiguration().postgresql_user
        self.__password = EnvConfiguration().postgresql_password
        self.__database = EnvConfiguration().postgresql_database
        self.__connection = None

    def __create_connection(self):
        try:
            self.__connection = psycopg2.connect(
                host=self.__host,
                port=self.__port,
                dbname=self.__database,
                user=self.__user,
                password=self.__password,
            )
            if not self.__connection:
                raise OperationalError
        except Exception as e:
            # TODO: solve better return
            print(f"Connection failed with PostgreSQL: {e}")
            self.__connection = None

    def client(self):
        if self.__connection is None:
            self.__create_connection()
        return self.__connection

    def close_connection(self):
        if self.__connection:
            self.__connection.close()
