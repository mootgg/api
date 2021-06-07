from fastapi import APIRouter

from .internal import router as internal_router
from .moots import router as moots_router

router = APIRouter(prefix="/v1")
router.include_router(moots_router)
router.include_router(internal_router)
