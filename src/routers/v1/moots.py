from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.models.api import Moot, NewMoot
from src.utils.types import Request

router = APIRouter(prefix="/moots")


@router.post("/", response_model=Moot)
async def new_moot(data: NewMoot, request: Request) -> Moot:
    """Create a new Moot."""

    request.state.auth.raise_for_user()

    moot = await request.state.db.create_moot(
        request.state.ids.next(), data.content, request.state.auth.auth.user
    )
    return moot.api_ready


@router.get("/{moot_id}", response_model=Moot)
async def get_moot(moot_id: int, request: Request) -> Moot:
    """Get a Moot by ID."""

    request.state.auth.raise_for_validity()

    moot = await request.state.db.get_moot(moot_id)
    if not moot:
        raise HTTPException(404)

    return moot.api_ready


@router.delete("/{moot_id}", response_model=Moot)
async def delete_moot(moot_id: int, request: Request) -> Moot:
    """Delete a Moot by ID."""

    request.state.auth.raise_for_validity()

    moot = await request.state.db.get_moot(moot_id)
    if not moot:
        raise HTTPException(404)

    if not request.state.auth.admin:
        if moot.author.id != request.state.auth.auth.user.id:
            raise HTTPException(403)

    await request.state.db.delete_moot(moot_id)

    return moot.api_ready
