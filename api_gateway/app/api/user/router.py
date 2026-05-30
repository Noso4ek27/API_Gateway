# api_gateway/app/api/user/router.py
# Запросы к таблице юзеров

from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api_gateway.app.api.schemas import UserCreate, UserResponse, UserRelatoinResponse, UserDelete
from api_gateway.app.db.session import get_db
from api_gateway.app.api.user import service
from api_gateway.app.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
    ) -> UserResponse:
    """
    Эндпоинт создания юзера
    Args:
        payload: схема pydantic UserCreate
        db: AsyncSession
    Returns:
        UserResponse: схема pydantic UserResponse
    """
    return await service.create_user(payload, db)


@router.get("/get", response_model=UserResponse, )      #добавить статус кода
async def get_user_endpoint(
    email: EmailStr,
    db: AsyncSession = Depends(get_db)
    ) -> UserResponse:
    """
    Эндпоинт получения юзера
    Args:
        payload: схема pydantic UserCreate
        db: AsyncSession
    Returns:
        UserResponse: схема pydantic UserResponse
    """
    user = await service.get_user(email, db)           
    return user



@router.delete("/delete", response_model=UserDelete, )   
async def delete_user_endpoint(
    email: EmailStr,
    db: AsyncSession = Depends(get_db)
    ) -> UserDelete:
    """
    Эндпоинт удаления юзера по email.
    
    Args:
        email: EmailStr (Query параметр)
        db: AsyncSession
        
    Returns:
        UserDelete: Схема pydantic с количестом удалённых пользователей
    """
    try:
        return await service.delete_user(email, db)
    except Exception as e:
        logger.exception(f"Unexpected error while deleting user: {e}")
        raise