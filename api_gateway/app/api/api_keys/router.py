# api_gateway/app/api/api_keys/router.py
# Запросы к таблице ключей

from uuid import UUID
from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api_gateway.app.api.schemas import ApiKeysCreate, ApiKeysResponse
from api_gateway.app.db.session import get_db
from api_gateway.app.api.api_keys import service
from api_gateway.app.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

router = APIRouter()

@router.post("/user/{user_id}/api-keys",
            response_model=ApiKeysResponse,
)
async def create_apikey_endpoint(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
    ) -> ApiKeysResponse:
    """

    """
    return await service.create_api_key(user_id = user_id, db = db)

@router.get(
    "/user/{user_id}/api-keys",
    response_model= list[ApiKeysResponse]
)
async def get_apikeys_endpoint(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
    ) -> list[ApiKeysResponse]:
    """

    """
    return await service.list_api_keys(user_id = user_id, db = db)

@router.delete(
    "/user/{user_id}/api-keys/{api_key_id}",
)
async def deactivate_api_key(
    user_id: UUID,
    api_key_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await service.disable_api_key(
        user_id=user_id,
        api_key_id=api_key_id,
        db=db,
    )