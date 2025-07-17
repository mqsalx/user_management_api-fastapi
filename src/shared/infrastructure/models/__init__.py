# /src/shared/infrastructure/models/__init__.py

def configure_all_mappers():
    """
    Configures all SQLAlchemy mappers before initializing the ORM.

    This function ensures that SQLAlchemy's declarative models are fully
    configured and all relationships between models are properly established
    before any operations such as migrations or queries are executed.

    It is especially useful when using separate modules for models and
    avoiding circular import issues.

    Note:
        Although some model imports are commented out, they should be
        uncommented and included when those models are active in the project.
    """
    from src.modules.user.infrastructure.models.user import UserModel
    # from src.modules.auth.infrastructure.models.role import RoleModel
    # from src.modules.auth.infrastructure.models.permission import PermissionModel
    # from src.modules.auth.infrastructure.models.session import SessionModel
    # from src.modules.auth.infrastructure.models.token import TokenModel

    from sqlalchemy.orm import configure_mappers
    configure_mappers()
