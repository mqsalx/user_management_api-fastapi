# /src/data/models/auth/session/__init__.py

# flake8: noqa: E501

# PY
import uuid

from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import relationship

# Core
from src.core.configurations import DatabaseConfig

# Data
from src.data.models import SessionAuthModel

# Utils
from src.utils.generator import GenUtil

Base = DatabaseConfig.base()


class TokenModel(Base):
    """
    """
    __tablename__ = "tokens"

    token_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
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

    sessions_auth = relationship(
        SessionAuthModel,
        backref="tokens",
        cascade="all, delete-orphan"
    )
