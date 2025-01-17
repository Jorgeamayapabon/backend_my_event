from fastapi import APIRouter
from .user import router as user_router
from .location import router as location_router
from .event import event_router
from .event import session_router
from .category import router as category_router

# Create the main API router for the application
api_router = APIRouter()

# Include the User router
api_router.include_router(user_router, prefix="/user", tags=["User"])
"""
Includes routes related to user operations under the "/user" prefix.
Tagged as "User" for better documentation and organization.
"""

# Include the Location router
api_router.include_router(location_router, prefix="/location", tags=["Location"])
"""
Includes routes related to location operations under the "/location" prefix.
Tagged as "Location" for better documentation and organization.
"""

# Include the Event router
api_router.include_router(event_router, prefix="/event", tags=["Event"])
"""
Includes routes related to event operations under the "/event" prefix.
Tagged as "Event" for better documentation and organization.
"""

# Include the Session router
api_router.include_router(session_router, prefix="/session", tags=["Session"])
"""
Includes routes related to session operations under the "/session" prefix.
Tagged as "Session" for better documentation and organization.
"""

# Include the Category router
api_router.include_router(category_router, prefix="/category", tags=["Category"])
"""
Includes routes related to category operations under the "/category" prefix.
Tagged as "Category" for better documentation and organization.
"""
