import os

import psycopg
import redis
from fastapi import FastAPI

app = FastAPI(title="API Gateway")


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "")


def get_redis_url() -> str:
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/infra")
def health_infra() -> dict[str, str]:
    database_url = get_database_url()
    redis_url = get_redis_url()

    db_status = "ok"
    redis_status = "ok"

    try:
        with psycopg.connect(database_url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
    except Exception:
        db_status = "error"

    try:
        redis_client = redis.Redis.from_url(redis_url, socket_connect_timeout=3)
        redis_client.ping()
    except Exception:
        redis_status = "error"

    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status,
    }
