from fastapi import APIRouter, Request

from src.models.api import Moot, NewMoot


router = APIRouter(prefix="/moots")

@router.post("/", response_model=Moot)
async def new_moot(data: NewMoot, request: Request) -> Moot:
    """Create a new Moot."""

    pass

@router.get("/{moot_id}", response_model=Moot)
async def get_moot(moot_id: int, request: Request) -> Moot:
    """Get a Moot by ID."""

    pass

@router.delete("/{moot_id}", response_model=Moot)
async def delete_moot(moot_id: int, request: Request) -> Moot:
    """Delete a Moot by ID."""

    pass
