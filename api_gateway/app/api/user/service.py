# api_gateway/app/api/user/service.py
# сами функции запросов 

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import asyncio

from api_gateway.app.api.schemas import UserCreate, UserResponse, UserRelatoinResponse, UserDelete
from api_gateway.app.db.session import db_client, get_db
from api_gateway.app.utils.logger import setup_logging, get_logger
from api_gateway.app.db.models import Users

setup_logging()
logger = get_logger(__name__)

async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),) -> Users:
    """
    Функция создания юзера в таблице юзерс
    Args:
        db: AsyncSession
        payload: схема pydantic UserCreate
    """
    try:
        user = Users(email=payload.email)
        db.add(user)
        await db.commit()
        logger.info(f"Юзер {user.email} создан")
        await db.refresh(user)
        return user
    except Exception as e:
        logger.exception(f"Ошибка создания юзера: {e}")
        raise

async def get_user(
    email: EmailStr,
    db: AsyncSession = Depends(get_db),) -> Users|None:
    """
    Функция получения юзера из таблицы юзерс
    Args:
        db: AsyncSession
        payload: схема pydantic UserResponse
    """
    try:
        response = (select(Users).filter(Users.email == email))
        user = await db.execute(response)
        return user.scalar_one_or_none()
    except Exception as e:
        logger.exception(f"Ошибка получения юзера: {e}")
        raise

async def get_user_with_relation(
    payload: UserRelatoinResponse,
    db: AsyncSession = Depends(get_db),):
    """
    Функция получения юзера с отношением к таблице api_keys
    Args:
        db: AsyncSession
        payload: схема pydantic UserRelatoinResponse
    """
    ...

async def delete_user(
    email: EmailStr,
    db: AsyncSession = Depends(get_db),) -> int:
    """
    Функция удаления юзера
    Args:
        db: AsyncSession
        payload: схема pydantic UserCreate
    """
    try:
        response = delete(Users).where(Users.email == email)
        result = await db.execute(response)
        await db.commit()
        return {"counts":result.rowcount}

    except Exception as e:
        logger.exception(f"Удаление User не удалось: {e}")
        raise

async def test():
    async with db_client.session() as session:
        payload = UserCreate(email="test@test.com")
        res = await delete_user(db=session, payload=payload)
        logger.info(f"Юзеров удалено: {res}")        

        payload = UserCreate(email="test@test.com")
        res = await create_user(db=session, payload=payload)
        logger.info(f"Юзер создан с ID: {res.id}")

        payload = UserCreate(email='test@test.com')
        res = await get_user(db=session, payload=payload)
        logger.info(f"Юзер получен с ID: {res.id}, временем создания: {res.created_at}")

if __name__ == "__main__":
    asyncio.run(test())
