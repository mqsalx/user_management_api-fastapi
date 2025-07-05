
# flake8: noqa: E501

# PY

from pathlib import Path
import importlib.util
import sys
import glob
import importlib
import importlib.util
import os
import pkgutil

from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, inspect, pool, text

# Core
from src.core.configurations.database import db_config
from src.core.configurations.database.utils import (
    DatabaseConfigUtil,
)

Base = db_config.base()

# Dynamically load models

try:
    base_path = Path(__file__).resolve().parent.parent / "src"
    print(f"Base path for models: {base_path}")

    with_modules_path = base_path / "modules"
    without_modules_path = base_path / "infrastructure" / "models"

    model_paths = list(with_modules_path.rglob("*/infrastructure/models/*.py"))
    model_paths += list(with_modules_path.glob("*/infrastructure/models/*.py"))
    model_paths += list(without_modules_path.rglob("*.py"))
    model_paths += list(without_modules_path.glob("*.py"))

    if not model_paths:
        print("No model files found in the expected directories.")
    else:
        print("Model files found:")
        for p in model_paths:
            print(f" - {p}")

    for model_file in model_paths:
        module_name = f"{model_file.stem}_{model_file.parent.name}"
        print(f"Importing module: {module_name} from {model_file}")

        spec = importlib.util.spec_from_file_location(module_name, str(model_file))
        module = importlib.util.module_from_spec(spec)
        if spec.loader:
            spec.loader.exec_module(module)

except Exception as error:
    raise ImportError(
        f"Failed to import models from the specified directories: {error}"
    ) from error

# Define the database URL
DATABASE_URL = DatabaseConfigUtil().get_url()

# Alembic configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Retrieve metadata from SQLAlchemy models
target_metadata = Base.metadata

print("Target metadata schema:", target_metadata.schema)

def include_name_filter(name: str, type_: str, parent_names: dict | None) -> bool:
    """
    Filter function for Alembic to include object names in autogeneration.

    This function ensures that only names from the target schema are included during migration.

    Args:
        name (str): The name of the database object (e.g., table, index).
        type_ (str): The type of the object (e.g., 'table', 'index').
        parent_names (dict | None): Parent information including schema name.

    Returns:
        bool: True if the object should be included, False otherwise.
    """
    if not parent_names:
        return True  # Defensive fallback

    target_schema = str(target_metadata.schema)
    current_schema = parent_names.get("schema_name")

    return current_schema == target_schema

def run_migrations_offline() -> None:
    _url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=target_metadata.schema,
        include_name=include_name_filter,
        include_schemas=True,
        compare_server_default=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Create schema if it doesn't exist
        if target_metadata.schema:
            connection.execute(
                text(f"CREATE SCHEMA IF NOT EXISTS {target_metadata.schema}")
            )
            connection.commit()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=target_metadata.schema,
            include_name=include_name_filter,
            include_schemas=True,
            compare_server_default=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    print("Migrations completed successfully!")

# Determine whether to run in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
