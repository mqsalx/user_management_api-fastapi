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
from src.core.configurations.database import Base

# Utils
from src.utils.generator import GenUtil


class SessionAuthModel(Base):
    """
    """
    __tablename__ = "sessions_auth"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    token_id = Column(
        String,
        ForeignKey("tokens.token_id"),
        nullable=False
    )
    user_id = Column(
        String,
        ForeignKey(column="users.user_id"),
        nullable=False
    )
    login_at = Column(
        String,
        nullable=True,
        default=GenUtil.generate_formatted_datetime
    )
    logout_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
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
