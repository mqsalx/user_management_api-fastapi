from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.core.configurations.env_configuration import EnvConfiguration
from src.core.enums.user_role_enum import UserRoleEnum
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
    DatabaseConfigurationUtil,
)
from src.infrastructure.models.user_model import UserModel
from src.utils.any_utils import AnyUtils, generate_password_hash


class DatabaseUtil:
    """
    Utility class for database operations, including admin user creation.
    """

    __api_name = EnvConfiguration().api_name
    __api_user_administrator = EnvConfiguration().api_user_administrator
    __api_password_administrator = (
        EnvConfiguration().api_password_administrator
    )

    def __init__(self):
        _db_url = DatabaseConfigurationUtil().get_url()
        self.__database_type = EnvConfiguration().database_type
        self.__engine = create_engine(_db_url)

    def check_connection(self) -> None:
        """
        Check if the database connection is successful.
        """
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

    @classmethod
    def create_admin_user(cls) -> None:
        """
        Creates an administrator user if it does not already exist.
        """
        db: Session = next(DatabaseConfiguration.get_db())

        try:
            existing_user = (
                db.query(UserModel)
                .filter(UserModel.name == cls.__api_user_administrator)
                .first()
            )

            if not existing_user:
                new_user = UserModel(
                    name=cls.__api_user_administrator,
                    email=f"{cls.__api_user_administrator.lower()}@{cls.__api_name}.com",
                    password=generate_password_hash(
                        cls.__api_password_administrator,
                    ),
                    role=UserRoleEnum.SUPER_ADMINISTRATOR,
                    created_at=AnyUtils.generate_formatted_datetime(),
                )

                db.add(new_user)
                db.commit()

                print("Admin user created successfully!")
            else:
                print("Admin user already exists, skipping creation.")

        except Exception as e:
            db.rollback()
            print(f"Error creating admin user: {e}")

        finally:
            db.close()
