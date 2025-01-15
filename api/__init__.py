from fastapi import APIRouter
from .user import router as user_router
from .location import router as location_router
from .event import event_router
from .event import session_router
from .category import router as category_router


api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(location_router, prefix="/location", tags=["Location"])
api_router.include_router(event_router, prefix="/event", tags=["Event"])
api_router.include_router(session_router, prefix="/session", tags=["Session"])
api_router.include_router(category_router, prefix="/category", tags=["Category"])
