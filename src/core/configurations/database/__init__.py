# /src/core/configurations/database/__init__.py

# PY
from typing import Any, AsyncGenerator, Generator

# Sync
from sqlalchemy import Engine, MetaData, create_engine

# Async
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Config
from src.core.configurations.database.utils import DatabaseConfigUtil
from src.core.configurations.environment import env_config


class DatabaseConfig:
    """ """

    # Config
    _schema: str = env_config.database_schema
    _metadata: MetaData = MetaData(schema=_schema)

    # Sync
    _sync_db_url: str = DatabaseConfigUtil().get_url()
    _sync_engine: Engine = create_engine(_sync_db_url)
    _sync_session_local: sessionmaker[Session] = sessionmaker(
        autocommit=False, autoflush=False, bind=_sync_engine
    )

    # Async
    _async_db_url: str = DatabaseConfigUtil().get_async_url()
    _async_engine: AsyncEngine = create_async_engine(
        url=_async_db_url, echo=False, future=True
    )
    _async_session_local: async_sessionmaker[AsyncSession] = (
        async_sessionmaker(
            bind=_async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
        )
    )

    # Base
    _base = declarative_base(metadata=_metadata)

    # Methods Async
    @classmethod
    async def get_async_db(cls) -> AsyncGenerator[AsyncSession, None]:
        async with cls._async_session_local() as session:
            yield session

    @classmethod
    async def create_all_async(cls) -> None:
        async with cls._async_engine.begin() as conn:
            await conn.run_sync(cls._base.metadata.create_all)

    @classmethod
    def async_engine(cls) -> AsyncEngine:
        return cls._async_engine

    # End Methods Async

    # Methods Sync
    @classmethod
    def get_sync_db(cls) -> Generator[Session, None, None]:
        db: Session = cls._sync_session_local()
        try:
            yield db
        finally:
            db.close()

    @classmethod
    def create_all_sync(cls) -> None:
        cls._base.metadata.create_all(bind=cls._sync_engine)

    @classmethod
    def sync_engine(cls) -> Engine:
        return cls._sync_engine

    # End Methods Sync

    # Base
    @classmethod
    def base(cls) -> Any:
        return cls._base


db_config = DatabaseConfig()
