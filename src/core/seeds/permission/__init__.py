# /src/core/seeds/permission/__init__.py

# PY
from sqlalchemy.orm import Session

# Core
from src.core.configurations import db_config, env_config
from src.modules.auth.infrastructure.models import PermissionModel

# Utils
from src.utils.logger import log


def create_permissions() -> None:
    """
    Function responsible for creating permissions in the database.

    It reads predefined permission IDs from the environment
        configuration and inserts only the ones that
        don't already exist in the database.

    Returns:
        None
    """

    db: Session = next(db_config.get_sync_db())

    __permissions = env_config.api_role_permissions

    try:
        if not __permissions:
            return

        # Fetch existing permission IDs
        existing_permissions = {
            permission.permission_id
            for permission in db.query(PermissionModel).all()
        }

        # Filter new permissions to insert
        new_permissions = [
            PermissionModel(permission_id=permission)
            for permission in __permissions
            if permission not in existing_permissions
        ]

        if new_permissions:
            db.add_all(new_permissions)
            db.commit()
            log.info(f"{len(new_permissions)} permission(s) created.")
        else:
            log.info("No new permissions to create.")

    except Exception as error:
        db.rollback()
        log.error(f"Error in create_permissions: {error}")

    finally:
        db.close()
