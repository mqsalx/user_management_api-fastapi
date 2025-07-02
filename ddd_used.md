
Estrutura Domain Driven Design - FastAPI + SQLAlchemy + PostgreSQL
Estrutura de Diretórios
project_root/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── settings.py
│   ├── shared/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── base_entity.py
│   │   │   ├── value_objects.py
│   │   │   └── exceptions.py
│   │   ├── infrastructure/
│   │   │   ├── __init__.py
│   │   │   ├── base_repository.py
│   │   │   ├── database.py
│   │   │   └── unit_of_work.py
│   │   └── application/
│   │       ├── __init__.py
│   │       ├── base_service.py
│   │       └── interfaces/
│   │           ├── __init__.py
│   │           ├── repository.py
│   │           └── unit_of_work.py
│   ├── modules/
│   │   └── user/  # Exemplo de módulo
│   │       ├── __init__.py
│   │       ├── domain/
│   │       │   ├── __init__.py
│   │       │   ├── entities/
│   │       │   │   ├── __init__.py
│   │       │   │   └── user.py
│   │       │   ├── value_objects/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── email.py
│   │       │   │   └── user_id.py
│   │       │   ├── repositories/
│   │       │   │   ├── __init__.py
│   │       │   │   └── user_repository.py
│   │       │   └── services/
│   │       │       ├── __init__.py
│   │       │       └── user_domain_service.py
│   │       ├── application/
│   │       │   ├── __init__.py
│   │       │   ├── commands/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── create_user.py
│   │       │   │   └── update_user.py
│   │       │   ├── queries/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── get_user.py
│   │       │   │   └── list_users.py
│   │       │   ├── handlers/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── command_handlers.py
│   │       │   │   └── query_handlers.py
│   │       │   └── services/
│   │       │       ├── __init__.py
│   │       │       └── user_application_service.py
│   │       ├── infrastructure/
│   │       │   ├── __init__.py
│   │       │   ├── models/
│   │       │   │   ├── __init__.py
│   │       │   │   └── user_model.py
│   │       │   ├── repositories/
│   │       │   │   ├── __init__.py
│   │       │   │   └── user_repository_impl.py
│   │       │   └── mappers/
│   │       │       ├── __init__.py
│   │       │       └── user_mapper.py
│   │       └── presentation/
│   │           ├── __init__.py
│   │           ├── routers/
│   │           │   ├── __init__.py
│   │           │   └── user_router.py
│   │           ├── schemas/
│   │           │   ├── __init__.py
│   │           │   ├── user_request.py
│   │           │   └── user_response.py
│   │           └── dependencies/
│   │               ├── __init__.py
│   │               └── user_dependencies.py
│   └── api/
│       ├── __init__.py
│       ├── dependencies.py
│       ├── middleware.py
│       └── routes.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
Implementação dos Arquivos Base
1. app/config/settings.py
python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DDD FastAPI Project"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
2. app/config/database.py
python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
3. app/shared/domain/base_entity.py
python
from abc import ABC
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class BaseEntity(ABC):
    def __init__(self, entity_id: Optional[UUID] = None):
        self._id = entity_id or uuid4()
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def mark_as_updated(self):
        self._updated_at = datetime.utcnow()

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self._id == other._id
4. app/shared/domain/exceptions.py
python
class DomainException(Exception):
    """Base exception for domain errors"""
    pass

class ValidationException(DomainException):
    """Exception for validation errors"""
    pass

class EntityNotFoundException(DomainException):
    """Exception when entity is not found"""
    pass

class BusinessRuleViolationException(DomainException):
    """Exception for business rule violations"""
    pass
5. app/shared/application/interfaces/repository.py
python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from uuid import UUID

T = TypeVar('T')

class IRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        pass
6. app/shared/application/interfaces/unit_of_work.py
python
from abc import ABC, abstractmethod

class IUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
7. app/shared/infrastructure/unit_of_work.py
python
from sqlalchemy.orm import Session
from ..application.interfaces.unit_of_work import IUnitOfWork

class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: Session):
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        self._session.commit()

    async def rollback(self):
        self._session.rollback()
8. Exemplo de Entidade de Domínio: app/modules/user/domain/entities/user.py
python
from uuid import UUID
from typing import Optional
from app.shared.domain.base_entity import BaseEntity
from app.shared.domain.exceptions import ValidationException
from ..value_objects.email import Email
from ..value_objects.user_id import UserId

class User(BaseEntity):
    def __init__(
        self,
        name: str,
        email: Email,
        user_id: Optional[UserId] = None
    ):
        super().__init__(user_id.value if user_id else None)
        self._name = self._validate_name(name)
        self._email = email
        self._is_active = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> Email:
        return self._email

    @property
    def is_active(self) -> bool:
        return self._is_active

    def update_name(self, name: str):
        self._name = self._validate_name(name)
        self.mark_as_updated()

    def update_email(self, email: Email):
        self._email = email
        self.mark_as_updated()

    def activate(self):
        self._is_active = True
        self.mark_as_updated()

    def deactivate(self):
        self._is_active = False
        self.mark_as_updated()

    def _validate_name(self, name: str) -> str:
        if not name or len(name.strip()) < 2:
            raise ValidationException("Name must have at least 2 characters")
        return name.strip()
9. Value Object: app/modules/user/domain/value_objects/email.py
python
import re
from dataclasses import dataclass
from app.shared.domain.exceptions import ValidationException

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValidationException("Invalid email format")

    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def __str__(self) -> str:
        return self.value
10. Repository Interface: app/modules/user/domain/repositories/user_repository.py
python
from abc import abstractmethod
from typing import Optional, List
from app.shared.application.interfaces.repository import IRepository
from ..entities.user import User
from ..value_objects.email import Email

class IUserRepository(IRepository[User]):
    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    async def get_active_users(self) -> List[User]:
        pass
11. SQLAlchemy Model: app/modules/user/infrastructure/models/user_model.py
python
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
12. Repository Implementation: app/modules/user/infrastructure/repositories/user_repository_impl.py
python
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from ..models.user_model import UserModel
from ..mappers.user_mapper import UserMapper
from ...domain.entities.user import User
from ...domain.repositories.user_repository import IUserRepository
from ...domain.value_objects.email import Email

class UserRepositoryImpl(IUserRepository):
    def __init__(self, session: Session):
        self._session = session
        self._mapper = UserMapper()

    async def get_by_id(self, entity_id: UUID) -> Optional[User]:
        model = self._session.get(UserModel, entity_id)
        return self._mapper.to_entity(model) if model else None

    async def get_by_email(self, email: Email) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email.value)
        model = self._session.execute(stmt).scalar_one_or_none()
        return self._mapper.to_entity(model) if model else None

    async def get_all(self) -> List[User]:
        stmt = select(UserModel)
        models = self._session.execute(stmt).scalars().all()
        return [self._mapper.to_entity(model) for model in models]

    async def get_active_users(self) -> List[User]:
        stmt = select(UserModel).where(UserModel.is_active == True)
        models = self._session.execute(stmt).scalars().all()
        return [self._mapper.to_entity(model) for model in models]

    async def add(self, entity: User) -> User:
        model = self._mapper.to_model(entity)
        self._session.add(model)
        self._session.flush()
        return self._mapper.to_entity(model)

    async def update(self, entity: User) -> User:
        model = self._mapper.to_model(entity)
        self._session.merge(model)
        self._session.flush()
        return entity

    async def delete(self, entity_id: UUID) -> bool:
        model = self._session.get(UserModel, entity_id)
        if model:
            self._session.delete(model)
            return True
        return False
13. Command: app/modules/user/application/commands/create_user.py
python
from dataclasses import dataclass

@dataclass
class CreateUserCommand:
    name: str
    email: str
14. Command Handler: app/modules/user/application/handlers/command_handlers.py
python
from app.shared.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from ..commands.create_user import CreateUserCommand
from ...domain.entities.user import User
from ...domain.value_objects.email import Email
from ...domain.repositories.user_repository import IUserRepository

class UserCommandHandler:
    def __init__(self, user_repository: IUserRepository, uow: SQLAlchemyUnitOfWork):
        self._user_repository = user_repository
        self._uow = uow

    async def handle_create_user(self, command: CreateUserCommand) -> User:
        async with self._uow:
            email = Email(command.email)

            # Check if user already exists
            existing_user = await self._user_repository.get_by_email(email)
            if existing_user:
                raise ValueError("User with this email already exists")

            # Create new user
            user = User(name=command.name, email=email)
            created_user = await self._user_repository.add(user)

            await self._uow.commit()
            return created_user
15. FastAPI Router: app/modules/user/presentation/routers/user_router.py
python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..schemas.user_request import CreateUserRequest, UpdateUserRequest
from ..schemas.user_response import UserResponse
from ..dependencies.user_dependencies import get_user_command_handler, get_user_query_handler
from ...application.commands.create_user import CreateUserCommand
from ...application.handlers.command_handlers import UserCommandHandler

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    handler: UserCommandHandler = Depends(get_user_command_handler)
):
    try:
        command = CreateUserCommand(name=request.name, email=request.email)
        user = await handler.handle_create_user(command)
        return UserResponse.from_entity(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    # Implementation here
    pass

@router.get("/", response_model=List[UserResponse])
async def list_users():
    # Implementation here
    pass
16. app/main.py
python
from fastapi import FastAPI
from app.config.settings import settings
from app.modules.user.presentation.routers.user_router import router as user_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include routers
app.include_router(user_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to DDD FastAPI Application"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
17. alembic.ini
ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = postgresql://user:password@localhost/dbname

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
18. requirements.txt
txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
Comandos Úteis
Inicializar Alembic
bash
alembic init alembic
Criar migração
bash
alembic revision --autogenerate -m "Create user table"
Executar migrações
bash
alembic upgrade head
Executar aplicação
bash
uvicorn app.main:app --reload
Princípios DDD Implementados
Separação de Camadas: Domain, Application, Infrastructure, Presentation
Entidades: Objetos com identidade única
Value Objects: Objetos imutáveis sem identidade
Repositories: Abstração para persistência
Domain Services: Lógica de negócio que não pertence a uma entidade
Application Services: Orquestração de casos de uso
Unit of Work: Gerenciamento de transações
CQRS: Separação entre Commands e Queries
Esta estrutura fornece uma base sólida para desenvolvimento seguindo os princípios do Domain Driven Design com FastAPI.

Made with
