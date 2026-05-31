# api_gateway.app.api.me.router.py
# 

from fastapi import APIRouter, Request

from api_gateway.app.utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

router = APIRouter(
    tags = ["me"],
    )

@router.get("/me")
async def get_me(request: Request):
    return{
        "user_id": request.state.user.id,
        "email": request.state.user.email,
        "api-key": request.state.api_key
    }
