# 
#
from fastapi import APIRouter

from api_gateway.app.api.user.router import router as users_router
from api_gateway.app.api.health.router import router as health_router

router = APIRouter()

router.include_router(
    users_router,
    tags=["Users"],
)

router.include_router(
    health_router,
    tags=["Health"],
)