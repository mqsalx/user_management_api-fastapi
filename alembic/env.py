import importlib
import os
import pkgutil
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.database.database_configuration import DatabaseConfiguration
from src.infrastructure.database.database_configuration_util import DatabaseConfigurationUtil
from src.utils.database_util import DatabaseUtil

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
    models_path = os.path.dirname(importlib.import_module(models_package).__file__)
except AttributeError:
    raise ImportError(
        f"Could not find the package {models_package}. Ensure the 'models' folder contains an '__init__.py' file."
    )

for _, module_name, _ in pkgutil.iter_modules([models_path]):
    importlib.import_module(f"{models_package}.{module_name}")


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a database URL and no connection engine.
    Calls to context.execute() emit the given SQL statements as raw strings.
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
    Run migrations in 'online' mode.

    This method creates an engine and associates a connection with the Alembic context.
    The migration process runs within a transaction.
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

    print("✅ Migrations completed successfully! Now creating admin user...")

    from sqlalchemy import inspect
    from src.infrastructure.database.database_configuration import DatabaseConfiguration

    engine = DatabaseConfiguration._engine
    inspector = inspect(engine)

    if UserModel.__tablename__ in inspector.get_table_names():
        try:
            DatabaseUtil.create_admin_user()
        except Exception as e:
            print(f"⚠️ Error creating admin user: {e}")
    else:
        print("⚠️ Skipping admin user creation. 'users' table does not exist.")


# Determine whether to run in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
