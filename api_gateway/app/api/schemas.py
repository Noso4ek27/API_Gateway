# api_gateway/app/api/schemas.py
# схемы для моделей

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

from api_gateway.app.db.models import ApiKeys, Users

class UserCreate(BaseModel):
    """
    схема заполнения таблицы users
        email: EmailStr   "user@mail.ru"
    """
    email: EmailStr

class UserResponse(UserCreate):
    """
    Структура ответа бд пользователю.
        id: UUID
        email: EmailStr
        created_at: timestamp
    """
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDelete(BaseModel):
    """
    Структура ответа бд пользователю ghb elfktybb.
    """
    counts: int

class ApiKeysCreate(BaseModel):
    """
    Структура заполнения таблицы api_keys
    user_id: UUID
    key_hash: str
    rate_limit: int | None
    """
    user_id: UUID
    key_hash: str
    rate_limit: int | None


class ApiKeysResponse(ApiKeysCreate):
    """
    Структура ответа бд апи ключам.

    id: UUID
    user_id: UUID
    key_hash: str
    rate_limit: int
    is_active: bool
    created_at: datetime
    """
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ApiKeysResponseWithoutKey(BaseModel):
    """
    Структура ответа бд апи ключам.

    id: UUID
    user_id: UUID
    key_hash: str
    rate_limit: int
    is_active: bool
    created_at: datetime
    """
    user_id: UUID
    rate_limit: int
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RequestLogsCreate(BaseModel):
    """
    Структура заполнения таблицы request_logs

    api_key_id: UUID
    path: str
    method: str
    status_code: int
    latency_ms: int
    """
    api_key_id: UUID
    path: str
    method: str
    status_code: int
    latency_ms: int

class RequestLogsResponse(RequestLogsCreate):
    """
    Структура вывода таблицы request_logs

    api_key_id: UUID
    path: str
    method: str
    status_code: int
    latency_ms: int
    id: int
    created_at: datetime
    """
    id: int
    created_at: datetime


class UserRelatoinResponse(UserResponse):

    """
    Ответ бд с relationship
    """

    api_keys: list["ApiKeysResponse"]

class ApiKeysRelationResponse(ApiKeysResponse):
    """
    Ответ бд с relationship
    """

    user: "UserResponse"