# /src/infrastructure/repository/user_repository.py


from sqlalchemy.orm import Session

from src.core.enums.user_role_enum import UserRoleEnum
from src.infrastructure.models.user_model import UserModel


class UserRepository:

    def __init__(self, db: Session):
        self.__database = db

    def create_user(self, **kwargs) -> UserModel:
        try:

            user = UserModel(**kwargs)

            self.__database.add(user)

            self.__database.commit()

            self.__database.refresh(user)

            return user

        except Exception as error:
            self.__database.rollback()
            print(error)
            raise

    def find_user(self, user_id: str) -> UserModel | None:
        return (
            self.__database.query(UserModel)
            .filter(
                UserModel.user_id == user_id,
                UserModel.role != UserRoleEnum.SUPER_ADMINISTRATOR,
            )
            .first()
        )

    def find_users(self) -> list[UserModel] | None:
        return (
            self.database.query(UserModel)
            .filter(UserModel.role != UserRoleEnum.SUPER_ADMINISTRATOR)
            .all()
        )

    def remove_user(self, user: UserModel) -> None:
        try:

            self.__database.delete(user)

            self.__database.commit()

        except Exception as error:
            self.__database.rollback()
            print(error)
            raise

    def find_user_email(self, email: str) -> UserModel:
        return (
            self.__database.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

    @property
    def database(self) -> Session:
        return self.__database
