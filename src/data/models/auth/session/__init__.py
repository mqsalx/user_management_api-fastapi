# /src/data/models/auth/session/__init__.py

# flake8: noqa: E501

# PY
import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String
)

# Core
from src.core.configurations import DatabaseConfig

# Utils
from src.utils.generator import GenUtil

Base = DatabaseConfig.base()

class SessionAuthModel(Base):
    """
    """
    __tablename__ = "sessions_auth"

    session_auth_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    jti = Column(String, nullable=False, unique=True)
    user_id = Column(
        String,
        ForeignKey("users.user_id"),
        nullable=False
    )
    access_token = Column(String, nullable=False, unique=True)
    created_at = Column(
        String,
        nullable=False,
        default=GenUtil.generate_formatted_datetime
    )
    updated_at = Column(
        String,
        nullable=False,
        default=GenUtil.generate_formatted_datetime,
        onupdate=GenUtil.generate_formatted_datetime,
    )
    is_active = Column(Boolean, default=True, nullable=False)
    logout_at = Column(DateTime, nullable=True)
