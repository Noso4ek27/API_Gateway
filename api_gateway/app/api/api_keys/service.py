# api_gateway.app.api.api_keys.service.py
#

from uuid import UUID
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import asyncio

from api_gateway.app.api.schemas import ApiKeysResponse, ApiKeysCreate, ApiKeysResponseWithoutKey, UserResponse
from api_gateway.app.db.session import db_client, get_db
from api_gateway.app.utils.logger import setup_logging, get_logger
from api_gateway.app.db.models import Users, ApiKeys
from api_gateway.app.services.api_key_serv import hash_api_key, generate_api_key
from api_gateway.app.api.user.service import get_user_UUID, UserNotFoundException

setup_logging()
logger = get_logger(__name__)


async def disable_api_key(
    user_id: UUID,
    api_key_id: UUID,
    db: AsyncSession) -> bool: 
    """
    Отключает апи ключ(флаг в бд)
    """
    try:
        query = (select(ApiKeys)
                .where(ApiKeys.id == api_key_id,
                ApiKeys.is_active == True))
        result = await db.execute(query)
        api_key_record = result.scalar_one_or_none()

        if api_key_record is None:
            raise UserNotFoundException(user_id = api_key_id, message = "Такого ключа нет")
            
            

        api_key_record.is_active = False
        logger.info(f"Ключ: {api_key_id} disable")
        await db.commit()
        return True
    except UserNotFoundException:
        raise
    except Exception as e:
        await db.rollback()
        logger.exception(f"Api key status error: {e}")
        raise

async def create_api_key(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
    ) -> ApiKeysResponse:
    """
    Создаёт API ключ для пользователя
    """

    try: 
        user = await get_user_UUID(user_id, db = db)

        user = user
        if user is None:
            raise UserNotFoundException(user_id = user_id)

        api_key = await generate_api_key()
        hashed_key = await hash_api_key(api_key)

        key_rec = ApiKeys(user_id = user_id,
                    key_hash = hashed_key)

        db.add(key_rec)
        await db.commit()
        logger.info(f"Ключ для пользователя {user_id} создан")
        await db.refresh(key_rec)
        
        return ApiKeysResponse(
            id = key_rec.id,
            user_id = user_id,
            key_hash = api_key,
            rate_limit = key_rec.rate_limit,
            is_active = key_rec.is_active,
            created_at = key_rec.created_at
        )
    except UserNotFoundException:
        raise
    except Exception as e:
        logger.exception(f"API_key create failed: {e}")
        raise

async def list_api_keys(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    ) -> list[ApiKeys]: #заполнить докстринг
    """

    """

    try:
        user = await get_user_UUID(user_id, db = db)

        if user is None:
            raise UserNotFoundException(user_id = user_id)
        
        response = (select(ApiKeys)
                    .where(ApiKeys.user_id == user_id))

        keys = await db.execute(response)
        return keys.scalars().all()
    except UserNotFoundException:
        raise
    except Exception as e:
        logger.exception(f"list api keys error: {e}")
        raise

async def search_user(
    key_hash: str,
    db: AsyncSession
    ) -> UserResponse:
    """

    """
    try:
        response = (select(ApiKeys.user_id)
                    .select_from(ApiKeys)
                    .where(ApiKeys.key_hash == key_hash, 
                    ApiKeys.is_active == True,))
        result = (await db.execute(response)).scalar_one_or_none()
        if result is None:
            raise UserNotFoundException(user_id = key_hash)
        
        response_user = (select(Users)
                        .where(Users.id == result))
        result_user = (await db.execute(response_user)).scalar_one_or_none()
        if result_user is None:
            raise UserNotFoundException(user_id = key_hash)

        return UserResponse.model_validate(result_user)

    except UserNotFoundException:
        raise
    except Exception as e:
        raise

# async def main():
#     async with db_client.session() as session:
#         try:

#             TEST_USER_UUID = UUID("5616afd9-3be3-4c6a-97b2-7c694fbba96a") 
            
#             print(f"\n1. Тест создания API-ключа для юзера: {TEST_USER_UUID}")
#             new_key_data = await create_api_key(user_id=TEST_USER_UUID, db=session)
#             print(f"[УСПЕХ] Ключ создан!")
#             print(f"Чистый ключ: {new_key_data.key_hash}")
            
#             # 2. Тестируем вывод списка ключей
#             print(f"\n2. Тестируем получение списка ключей для юзера...")
#             user_keys = await list_api_keys(user_id=TEST_USER_UUID, db=session)
#             print(f"[УСПЕХ] Найдено ключей в базе: {len(user_keys)}")
#             for k in user_keys:
#                 print(f" - ID ключа: {k.id} | Хеш в БД: {k.key_hash[:10]}... | Активен: {k.is_active}")

#             # 3. Тестируем отключение ключа
#             print(f"\n3. Тестируем отключение созданного ключа...")
#             disabled = await disable_api_key(api_key=new_key_data.key_hash, db=session)
#             print(f"[РЕЗУЛЬТАТ] Ключ успешно отключен: {disabled}")
            
#         except UserNotFoundException as ex:
#             print(f"[ОШИБКА] Пользователь с UUID {ex.user_id} не найден. Пропиши валидный UUID в main()!")
#         except Exception as ex:
#             print(f"[ОШИБКА ТЕСТИРОВАНИЯ] Что-то пошло не так: {ex}")
async def main():
    async with db_client.session() as session:
        print(f"search_user {await search_user("348ea91a22bb78defd99bb028decd0c44147b0c2fa09ec6cb874fb23d4615651", session)}")

if __name__ == "__main__":
    # Запуск асинхронного цикла для выполнения теста прямо из терминала
    asyncio.run(main())