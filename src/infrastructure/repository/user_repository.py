# /src/infrastructure/repository/user_repository.py


from sqlalchemy.orm import Session

from src.infrastructure.models.user_model import UserModel


class UserRepository:

    def __init__(self, db: Session):
        self.__database = db

    def create_user(self, user_data: dict) -> UserModel:
        try:

            user = UserModel(
                name=user_data["name"],
                email=user_data["email"],
                status=user_data.get("status", "ACTIVE"),
                created_at=user_data["created_at"],
            )

            self.__database.add(user)

            self.__database.commit()

            self.__database.refresh(user)

            return user

        except Exception as error:
            print(error)
            raise

    # def get_user_by_id(self, user_id):
    #     return self.__dao.find_by_id(user_id)

    # def get_all_users(self):
    #     return self.__dao.find_all()

    # def update_user(self, user):
    #     self.__dao.update(user)

    # def delete_user(self, user_id):
    #     self.__dao.delete(user_id)
    #     self.__dao.delete(user_id)
    #     self.__dao.delete(user_id)
