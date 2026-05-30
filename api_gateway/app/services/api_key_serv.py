# api_gateway/app/servies/api_key_serv.py
#
import hashlib
import secrets
import string
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_gateway.app.db.models import ApiKeys
from api_gateway.app.utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

async def generate_api_key(lenthg: int = 32) -> str:
    """
    Функция генерации апи ключей
    Args:
        lenthg: int = 32 длина ключа

    Returns:
        key: str ключ
    """
    alphakey = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphakey) for _ in range(lenthg))

async def hash_api_key(api_key: str) -> str:
    """
    Хэширует ключ с помощью sha256
    """
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

async def verify_api_key(api_key: str, api_hash_from_db: str) -> bool:
    """
    Сравнивает отправленный ключ с хэшом из бд
    Args:
        api_key: str Api ключ пользователя
        api_hash_from_db: str Хэш 
    Return:
    """
    return secrets.compare_digest(hash_api_key(api_key), api_hash_from_db)

async def disable_api_key(api_key: str, db: AsyncSession) -> bool: #Не проверено
    """
    Отключает апи ключ(флаг в бд)
    """
    hashed_key = hash_api_key(api_key)

    try:
        query = (select(ApiKeys)
                .where(ApiKeys.key_hash == hashed_key,
                ApiKeys.is_active == True))
        result = await db.execute(query)
        api_key_record = result.scalar_one_or_none()

        if api_key_record is None:
            logger.info("Такого ключа нет(изменение активности)")
            return False
            

        api_key_record.is_active = False
        logger.info(f"Ключ: {hashed_key} disable")
        db.commit()
        return True
    
    except Exception as e:
        await db.rollback()
        logger.exception(f"Api key status error: {e}")
        raise

if __name__ == "__main__":
    key = generate_api_key()
    hash = hash_api_key(key)
    print(f"key: {key}")
    print(f"hash: {hash_api_key(key)}")
    print (f"verify: {verify_api_key(key, hash)}")
