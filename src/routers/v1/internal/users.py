from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from src.models.api import User, NewUser


router = APIRouter(prefix="/users")

@router.post("/", response_model=User, include_in_schema=False)
async def new_user(data: NewUser, request: Request) -> User:
    """Create a new user."""

    request.state.auth.raise_for_internal()

    try:
        user = await request.state.db.create_user(request.state.ids.next(), data.discord_id, data.username, data.avatar_hash)
    except UniqueViolationError:
        raise HTTPException(400, "User already exists.")
    return user.api_ready
