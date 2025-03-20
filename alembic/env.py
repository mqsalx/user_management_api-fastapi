import importlib
import os
import pkgutil
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from src.infrastructure.database.database_configuration import (
    DatabaseConfiguration,
)
from src.infrastructure.database.database_configuration_util import (
    DatabaseConfigurationUtil,
)
from src.infrastructure.models.permission_model import PermissionModel
from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.user_model import UserModel

# Define the database URL
DATABASE_URL = DatabaseConfigurationUtil().get_url()

# Alembic configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Retrieve metadata from SQLAlchemy models
target_metadata = DatabaseConfiguration.base().metadata

# Dynamically load models
models_package = "src.infrastructure.models"

try:
    models_path = os.path.dirname(
        importlib.import_module(models_package).__file__  # type: ignore
    )
except AttributeError:
    raise ImportError(
        f"Could not find the package {models_package}. Ensure the 'models' folder contains an '__init__.py' file."
    )

for _, module_name, _ in pkgutil.iter_modules([models_path]):
    importlib.import_module(f"{models_package}.{module_name}")


def run_migrations_offline() -> None:
    """
    Standalone Function responsible for running migrations in 'offline' mode.

    In this mode, Alembic generates SQL statements without requiring a database connection.

    Args:
        None

    Returns:
        None
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Standalone Function responsible for running migrations in 'online' mode.

    This method creates a database engine, establishes a connection, and
    runs the migration process within a transaction.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: If an error occurs during migration or table creation.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

    print("Migrations completed successfully!")

    from sqlalchemy import inspect

    engine = DatabaseConfiguration._engine
    inspector = inspect(engine)

    # Validate and create permissions
    if PermissionModel.__tablename__ in inspector.get_table_names():
        try:
            print("Creating permissions...")

            PermissionModel.create_permissions()

            print("Permissions created successfully!")

        except Exception as e:
            print(f"Error creating permissions: {e}")
    else:
        print(
            f"Skipping permission creation. {PermissionModel.__tablename__} table does not exist."
        )

    # Validate and create roles
    if RoleModel.__tablename__ in inspector.get_table_names():
        try:
            print("Creating roles...")

            RoleModel.create_roles()

            print("Roles created successfully!")

            print("Assigning permissions to administrator role...")

            RoleModel.assign_permissions_to_administrator()

            print("Permissions assigned to administrator role successfully!")
        except Exception as e:
            print(f"Error creating roles: {e}")
    else:
        print(
            f"Skipping roles creation. {RoleModel.__tablename__} table does not exist."
        )

    # Validate and create admin user
    if UserModel.__tablename__ in inspector.get_table_names():
        try:
            print("Creating admin user...")

            UserModel.create_administrator_user()

            print("Admin user created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {e}")
    else:
        print(
            f"Skipping admin user creation. {UserModel.__tablename__} table does not exist."
        )


# Determine whether to run in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
