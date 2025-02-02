# /src/infrastructure/repositories/user/user_dao.py

from src.infrastructure.dao.user_db_commands import UserDatabaseCommands


class UserMapper:

    def __init__(self, db_connection):
        self.__connection = db_connection
        self.__command = UserDatabaseCommands()

    def create_table(self):

        _create_command = self.__command.get_create_table_command()
        cursor = None

        try:
            cursor = self.__connection.cursor()
            cursor.execute(_create_command)
            self.__connection.commit()
        except Exception as e:
            print(f"Error to create table: {e}")
        finally:
            if cursor:
                cursor.close()

    def save(self, user_data: dict):

        _insert_command = self.__command.get_create_user_command(user_data)
        cursor = None

        try:
            cursor = self.__connection.cursor()
            cursor.execute(_insert_command)
            user_id = cursor.fetchone()[0]
            self.__connection.commit()
            print(f"User {user_data['name']} inserted successfully!")
            user_data["id"] = user_id
            return user_data
        except Exception as e:
            print(f"Error to save user: {e}")
        finally:
            if cursor:
                cursor.close()

    # def find_by_id(self, user_id):
    #     cursor = self.__connection.cursor()
    #     sql, params = UserMapper.get_user_by_id_sql(user_id)
    #     cursor.execute(sql, params)
    #     result = cursor.fetchone()
    #     cursor.close()
    #     return UserMapper.map_to_user(result)

    # def find_all(self):
    #     cursor = self.__connection.cursor()
    #     sql, params = UserMapper.get_all_users_sql()
    #     cursor.execute(sql, params)
    #     results = cursor.fetchall()
    #     cursor.close()
    #     return UserMapper.map_to_user_list(results)

    # def update(self, user):
    #     cursor = self.__connection.cursor()
    #     sql, params = UserMapper.update_user_sql(user)
    #     cursor.execute(sql, params)
    #     self.__connection.commit()
    #     cursor.close()

    # def delete(self, user_id):
    #     cursor = self.__connection.cursor()
    #     sql, params = UserMapper.delete_user_sql(user_id)
    #     cursor.execute(sql, params)
    #     self.__connection.commit()
    #     cursor.close()
