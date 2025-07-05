# /src/core/seeds/user/__init__.py

# PY
from sqlalchemy.orm import Session
from src.core.configurations import db_config, env_config
from src.utils.auth import AuthUtil
from src.utils.logger import log

# Models
from src.modules.auth.infrastructure.models import RoleModel
from src.modules.user.infrastructure.models import UserModel


def create_administrator_user() -> None:
    """
    Function responsible for creating an administrator user.

    If a user with the admin name doesn't exist, it creates one and assigns the
    'super_administrator' role.

    Returns:
        None
    """
    db: Session = next(db_config.get_db())

    try:
        admin_name = env_config.api_user_administrator
        admin_password = env_config.api_password_administrator
        api_name = env_config.api_name

        existing_user = (
            db.query(UserModel)
            .filter(UserModel.name == admin_name)
            .first()
        )

        if existing_user:
            log.info("Administrator user already exists, skipping creation.")
            return

        super_admin_role = (
            db.query(RoleModel)
            .filter(RoleModel.role_id == "super_administrator")
            .first()
        )

        if not super_admin_role:
            log.error("Super Administrator role not found.")
            return

        new_user = UserModel(
            name=admin_name,
            email=f"{admin_name.lower()}@{api_name}.com",
            password=AuthUtil.generate_password_hash(admin_password),
            role_id=super_admin_role.role_id
        )

        db.add(new_user)
        db.commit()

        log.info("Administrator user created successfully.")

    except Exception as error:
        db.rollback()
        log.error(f"Error creating administrator user: {error}")

    finally:
        db.close()
