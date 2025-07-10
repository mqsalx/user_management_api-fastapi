# /src/shared/infrastructure/models/__init__.py

def configure_all_mappers():

    from src.modules.user.infrastructure.models.user import UserModel
    from src.modules.auth.infrastructure.models.role import RoleModel
    from src.modules.auth.infrastructure.models.permission import PermissionModel
    from src.modules.auth.infrastructure.models.session import SessionModel
    from src.modules.auth.infrastructure.models.token import TokenModel

    from sqlalchemy.orm import configure_mappers
    configure_mappers()
