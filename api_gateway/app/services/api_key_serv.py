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
    return "sk-".join(secrets.choice(alphakey) for _ in range(lenthg))

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


if __name__ == "__main__":
    key = generate_api_key()
    hash = hash_api_key(key)
    print(f"key: {key}")
    print(f"hash: {hash_api_key(key)}")
    print (f"verify: {verify_api_key(key, hash)}")
