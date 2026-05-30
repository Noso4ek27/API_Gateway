# api_gateway/app/db/schemas.py
# схемы для моделей

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    схема заполнения таблицы users
        email: EmailStr   "user@mail.ru"
    """
    email: EmailStr

class UserResponse(BaseModel):
    """
    Структура ответа бд пользователю.
        id: UUID
        email: EmailStr
        created_at: timestamp
    """
    id: UUID
    email: EmailStr
    created_at: datetime