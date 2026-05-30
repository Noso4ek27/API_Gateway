# api_gateway/app/db/session.py
#

from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api_gateway.app.utils.logger import get_logger, setup_logging
from api_gateway.app.utils.settings import get_settings

setup_logging()
logger = get_logger()
settings = get_settings()

class DataBase():
    """
    Асинхронный клиент для PostgreSQL
    
    Args:
        database_url: ссылка подключения к БД
        engine: движок SQLAlchemy
        session_factory: фабрика сессий
    """
    def __init__(self, database_url: str = settings.DATABASE_URL):
        """
        Инициализация класса
        """
        self.database_url = database_url

        self.engine = create_async_engine(
            url = self.database_url,
            echo = True,
            pool_pre_ping=True,
            pool_size = 10,
        )   

        self.session_factory = async_sessionmaker(
            bind = self.engine,
            class_ = AsyncSession,
            expire_on_commit = False,
            autoflush = False
        )

        logger.info("Db were create")
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession,  None]:
        """
        Контекстный менеджер для сессий.
        Контекстный менеджер SQLAlchemy сам сделает rollback при ошибке и close при выходе.
        """
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                logger.exception(f"DateBase error: {e}")
                raise

    async def dispose(self):
        """Очистка пула соединений при остановке приложения"""
        await self.engine.dispose()
        logger.exception("Пулл соединений очищен")

db_client = DataBase()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для эндпоинтов FastAPI.
    Каждый запрос получает свою чистую сессию и закрывает её после ответа.
    """
    async with db_client.session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.exception(f"Database error: {e}")
            raise