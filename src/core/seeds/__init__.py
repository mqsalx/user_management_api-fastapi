# /src/core/seeds/__init__.py

# PY
from sqlalchemy import inspect

from core.configurations.database import DatabaseConfig

from src.core.seeds.user import create_administrator_user
from src.core.seeds.permission import create_permissions
from src.core.seeds.role import (
    create_roles,
    assign_permissions_to_administrator
)

# Models
from src.modules.auth.infrastructure.models import (
    PermissionModel,
    RoleModel
)
from src.modules.user.infrastructure.models import UserModel


def create_initial_data(schema: str) -> None:
    """
    Standalone Function responsible for creating initial data in the database.

    Args:
        schema (str): Schema to inspect
    """

    engine = DatabaseConfig.sync_engine()
    inspector = inspect(engine)

    existing_tables = inspector.get_table_names(schema=schema)


    # Validate and create permissions
    if PermissionModel.__tablename__ in existing_tables:
        try:
            print("Creating permissions...")

            create_permissions()

            print("Permissions created successfully!")

        except Exception as e:
            print(f"Error creating permissions: {e}")
    else:
        print(
            f"Skipping permission creation. {PermissionModel.__tablename__} table does not exist."
        )

    # Validate and create roles
    if RoleModel.__tablename__ in existing_tables:
        try:
            print("Creating roles...")

            create_roles()

            print("Roles created successfully!")

            print("Assigning permissions to administrator role...")

            assign_permissions_to_administrator()

            print("Permissions assigned to administrator role successfully!")
        except Exception as e:
            print(f"Error creating roles: {e}")
    else:
        print(
            f"Skipping roles creation. {RoleModel.__tablename__} table does not exist."
        )

    # Validate and create admin user
    if UserModel.__tablename__ in existing_tables:
        try:
            print("Creating admin user...")

            create_administrator_user()

            print("Admin user created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {e}")
    else:
        print(
            f"Skipping admin user creation. {UserModel.__tablename__} table does not exist."
        )
