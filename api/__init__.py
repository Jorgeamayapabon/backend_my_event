from fastapi import APIRouter
from .users import router as users_router
from .locations import router as locations_router
from .events import event_router as events_router
from .events import session_router as sessions_router
from .categories import router as categories_router


api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(locations_router, prefix="/locations", tags=["Locations"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(sessions_router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(categories_router, prefix="/categories", tags=["Categories"])
