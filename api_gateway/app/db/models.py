# api_gateway/app/db/models.py
# создание таблиц для бд

import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, UUID, ForeignKey, text, String

from api_gateway.app.utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

class Base(DeclarativeBase):
    """Базовый класс для всех будущих моделей (таблиц)"""
    pass


class Users(Base):
    """
    Таблица юзеров
    Хранит: 
        id: UUID - user id
        email: varchar - user email
        created_at: timestamp - time of created user accaunt
    """

    __tablename__ = "users"

    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default= text("gen_random_uuid()"),
    )

    email: Mapped[str] = mapped_column(
        String(256),
        index=True, 
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    )

    api_keys: Mapped[list["ApiKeys"]] = relationship(
        back_populates="users",
    )

class ApiKeys(Base):
    """
    Таблицв апи ключей
    """

    __tablename__ = "api_keys"

    id:Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default= text("gen_random_uuid()"),
    )

    user_id:Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    key_hash:... 

    rate_limit:Mapped[int] = mapped_column(
        default=5
    )

    is_active:Mapped[bool] = mapped_column(
        server_default=text("true")
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    )

    user: Mapped["Users"] = relationship(
        back_populates="api_keys"
    )

class RequestLogs(Base):
    """
    Таблица логов запросов
    """
    __tablename__ = "request_logs"
    
    
    pass
