#
#

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis 

from api_gateway.app.utils.logger import setup_logging, get_logger
from api_gateway.app.db.session import db_client, get_db
from api_gateway.app.utils.settings import get_settings

setup_logging()
logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health() -> dict[str, str]:
    """Простой хелсчек, что само приложение поднялось и отвечает"""
    return {"status": "ok"}


@router.get("/infra")
async def health_infra(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Глубокий хелсчек инфраструктуры (PostgreSQL + Redis)"""
    db_status = "ok"
    redis_status = "ok"

    try:
        await db.execute(text("SELECT 1;"))
    except Exception as e:
        logger.error(f"Ошибка проверки базы данных в хелсчеке: {e}")
        db_status = "error"

    try:

        redis_client = aioredis.from_url(
            settings.REDIS_URL,  
            socket_timeout=3
        )
        await redis_client.ping()
        await redis_client.close()
    except Exception as e:
        logger.error(f"Ошибка проверки Redis в хелсчеке: {e}")
        redis_status = "error"

    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status,
    }