
# flake8: noqa: E501

# PY
import glob
import importlib
import importlib.util
import os
import pkgutil

from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text

# Core
from src.core.configurations.database import DatabaseConfig
from src.core.configurations.database.utils import (
    DatabaseConfigUtil,
)

# Data
from src.data.models.permission import PermissionModel
from src.data.models.role import RoleModel

# Dynamically load models
models_package = "src.modules.models"

    # models_path = os.path.dirname(
    #     importlib.import_module(models_package).__file__  # type: ignore
    # )
try:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "modules"))
    print(f"Base path for models: {base_path}")

    # for root, dirs, files in os.walk(base_path):
    #     for file in files:
    #         if file.endswith(".py"):
    #             full_path = os.path.join(root, file)
    #             print(f"📄 Encontrado: {full_path}")

    pattern = os.path.join(base_path, "*", "infrastructure", "model", "*.py")
    print(f"Pattern for model files: {pattern}")
    model_paths = glob.glob(pattern)
    print(f"Found model files: {model_paths}")
    # for model_file in model_paths:
    #     module_name = model_file.replace("/", ".").replace("\\", ".").rstrip(".py")
    #     print(f"Importing model file: {model_file} as module: {module_name}")
    #     spec = importlib.util.spec_from_file_location(module_name, model_file)
    #     module = importlib.util.module_from_spec(spec)
    #     if spec.loader:
    #         spec.loader.exec_module(module)
except Exception as error:
    raise ImportError(
        f"Error importing model files: {error}"
    )

# for _, module_name, _ in pkgutil.iter_modules([models_path]): # type: ignore
#     importlib.import_module(f"{models_package}.{module_name}")

# Define the database URL
DATABASE_URL = DatabaseConfigUtil().get_url()

# Alembic configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Retrieve metadata from SQLAlchemy models
target_metadata = DatabaseConfig.base().metadata

def run_migrations_offline() -> None:
    """
    Standalone Function responsible for running migrations in 'offline' mode.

    In this mode, Alembic generates SQL statements without requiring a database connection.

    Args:
        None

    Returns:
        None
    """
    from src.core.configurations.environment import env_config
    _schema = env_config.database_schema
    _url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=_schema,
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
    from src.core.configurations.environment import env_config

    _schema = env_config.database_schema

    connectable = engine_from_config(
        configuration=config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        if _schema:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{_schema}"'))
            connection.execute(text(f'SET search_path TO "{_schema}"'))
            connection.commit()

        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

    print("Migrations completed successfully!")

    from sqlalchemy import inspect

    engine = DatabaseConfig._engine
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

    from src.modules.user.infrastructure.model import UserModel

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
