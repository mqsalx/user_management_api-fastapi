# /src/infrastructure/dao/user_db_commands.py


class UserDatabaseCommands:

    def __init__(self, table_name="users"):
        self.__table_name = table_name

    def get_create_table_command(self):

        return f"""
        CREATE TABLE IF NOT EXISTS {self.__table_name} (
            id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            status VARCHAR(100) DEFAULT 'inactive',
            created_at VARCHAR(100),
            updated_at VARCHAR(100)
        );
        """

    def get_create_user_command(self, user_data):

        return f"""
            INSERT INTO users (id, name, email, status, created_at, updated_at)
            VALUES (
                '{user_data['id']}',
                '{user_data['name']}',
                '{user_data['email']}',
                '{user_data['status']}',
                '{user_data['created_at']}',
                '{user_data['updated_at']}'
            )
            RETURNING id;
        """

    # def get_insert_user_command(self, name, email):
    #     return f"""
    #     INSERT INTO {self.table_name} (name, email, created_at, updated_at)
    #     VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id;
    #     """

    # def get_update_user_command(self, user_id, name=None, email=None):
    #     updates = []
    #     if name:
    #         updates.append(f"name = '{name}'")
    #     if email:
    #         updates.append(f"email = '{email}'")
    #     updates_str = ", ".join(updates)
    #     return f"""
    #     UPDATE {self.table_name}
    #     SET {updates_str}, updated_at = CURRENT_TIMESTAMP
    #     WHERE id = %s;
    #     """

    # def get_select_user_by_id_command(self, user_id):
    #     return f"""
    #     SELECT id, name, email, created_at, updated_at
    #     FROM {self.table_name}
    #     WHERE id = %s;
    #     """

    # def get_select_all_users_command(self):
    #     return f"""
    #     SELECT id, name, email, created_at, updated_at
    #     FROM {self.table_name};
    #     """
