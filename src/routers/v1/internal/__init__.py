from fastapi import APIRouter

from .sessions import router as sessions_router
from .users import router as users_router

router = APIRouter(prefix="/internal")
router.include_router(users_router)
router.include_router(sessions_router)
