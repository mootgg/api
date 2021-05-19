from fastapi import APIRouter

from .moots import router as moots_router


router = APIRouter(prefix="/v1")
router.include_router(moots_router)
