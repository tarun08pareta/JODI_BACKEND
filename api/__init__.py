from api.auth import router as auth_router
from api.profiles import router as profiles_router
from api.messages import router as messages_router

__all__ = [
    "auth_router",
    "profiles_router", 
    "messages_router"
]
