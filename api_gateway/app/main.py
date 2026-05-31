from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from api_gateway.app.api.user.service import UserAlreadyExistsException, UserNotFoundException

from api_gateway.app.utils.logger import setup_logging, get_logger
from api_gateway.app.utils.settings import get_settings
from api_gateway.app.api.router import router
from api_gateway.app.middleware.auth import AuthMiddleware

setup_logging()
logger = get_logger(__name__)
settings = get_settings()

logger.info("Инициализация API")
app = FastAPI(
    title="API Gateway",
)

app.add_middleware(AuthMiddleware)

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )

@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"Email '{exc.email}' is already registered."}
    )

app.include_router(router)
