from fastapi import APIRouter

from .moots import router as moots_router
from .internal import router as internal_router


router = APIRouter(prefix="/v1")
router.include_router(moots_router)
router.include_router(internal_router)
