import psycopg
import redis
from fastapi import FastAPI

from api_gateway.app.utils.logger import setup_logging, get_logger
from api_gateway.app.utils.settings import get_settings

setup_logging()
logger = get_logger(__name__)
settings = get_settings()


app = FastAPI(title="API Gateway")
logger.info("Инициализация API")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/infra")
def health_infra() -> dict[str, str]:
    database_url = settings.DATABASE_URL
    redis_url = settings.REDIS_URL

    db_status = "ok"
    redis_status = "ok"

    try:
        with psycopg.connect(database_url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
    except Exception:
        logger.info("Ошибка в инициализации бд")
        db_status = "error"

    try:
        redis_client = redis.Redis.from_url(redis_url, socket_connect_timeout=3)
        redis_client.ping()
    except Exception:
        logger.info("Ошибка в инициализации редис")
        redis_status = "error"

    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status,
    }
