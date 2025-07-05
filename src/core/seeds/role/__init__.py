from sqlalchemy.orm import Session
from src.core.configurations import db_config, env_config
from src.modules.auth.infrastructure.models import (
    RoleModel,
    PermissionModel
)

from src.utils.logger import log


def create_roles() -> None:
    """
    Creates roles based on environment configuration.
    """
    db: Session = next(db_config.get_db())
    __roles = env_config.api_user_roles

    try:
        if not __roles:
            log.warning("No roles defined in environment configuration.")
            return

        existing_roles = {role.role_id for role in db.query(RoleModel).all()}

        new_roles = [
            RoleModel(role_id=role)
            for role in __roles
            if role not in existing_roles
        ]

        if new_roles:
            db.add_all(new_roles)
            db.commit()
            log.info(f"{len(new_roles)} role(s) created.")
        else:
            log.info("No new roles to create.")

    except Exception as error:
        db.rollback()
        log.error(f"Error creating roles: {error}")

    finally:
        db.close()


def assign_permissions_to_administrator() -> None:
    """
    Assigns all permissions to the 'administrator' role.
    """
    db: Session = next(db_config.get_db())

    try:
        administrator_role = (
            db.query(RoleModel).filter_by(role_id="administrator").first()
        )

        if not administrator_role:
            log.warning("Administrator role not found.")
            return

        all_permissions = db.query(PermissionModel).all()

        if not all_permissions:
            log.warning("No permissions found in database.")
            return

        administrator_role.permissions = all_permissions
        db.commit()

        log.info(f"{len(all_permissions)} permission(s) assigned to administrator role.")

    except Exception as error:
        db.rollback()
        log.error(f"Error assigning permissions: {error}")

    finally:
        db.close()
