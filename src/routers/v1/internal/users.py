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
        user = await request.state.db.create_user(
            request.state.ids.next(), data.discord_id, data.username, data.avatar_hash
        )
    except UniqueViolationError:
        raise HTTPException(400, "User already exists.")
    return user.api_ready


@router.delete("/{user_id}", response_model=User, include_in_schema=False)
async def delete_user(user_id: int, request: Request) -> User:
    """Delete a user by ID."""

    request.state.auth.raise_for_internal()

    user = await request.state.db.get_user(user_id)
    if not user:
        raise HTTPException(404)

    await request.state.db.delete_user(user_id)

    return user.api_ready
