# api_gateway.app.middleware.auth.py


from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api_gateway.app.services.api_key_serv import hash_api_key
from api_gateway.app.db.session import get_db, db_client
from api_gateway.app.api.api_keys.service import search_user
from api_gateway.app.utils.logger import setup_logging, get_logger
from api_gateway.app.api.user.service import UserNotFoundException

setup_logging()
logger = get_logger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:

        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "API Key is missing"}
            )
        
        hashed_key = await hash_api_key(api_key) #по идее можно было делать не асинхронно
        
        
        try:
            async with db_client.session() as db:
                user = await search_user(hashed_key, db)

            request.state.user =  user
            request.state.api_key = api_key
            request.state.hash = hashed_key

        except UserNotFoundException:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid API Key"}
            )
        except Exception as e:
            logger.error(f"AuthMiddelware error: {e}")
            raise

        return await call_next(request)

