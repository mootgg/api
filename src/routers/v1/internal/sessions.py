from datetime import datetime, timedelta
from secrets import token_hex

from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from src.models.api import Session, User
from src.utils.oauth import get_user_details


router = APIRouter(prefix="/sessions")

@router.post("/{token}", response_model=Session, include_in_schema=False)
async def new_session(token: str, request: Request) -> Session:
    """Create a new user session."""

    request.state.auth.raise_for_internal()
    raw_user = await get_user_details(request.state.sess, token)

    user = await request.state.db.get_user(int(raw_user["id"]))

    if not user:
        user = await request.state.db.create_user(
            request.state.ids.next(),
            int(raw_user["id"]),
            raw_user["username"] + "#" + raw_user["discriminator"],
            raw_user.get("avatar", None)
        )

    session_token = token_hex(64)
    expires = datetime.utcnow() + timedelta(days=7)

    async with request.state.db.pool.acquire() as conn:
        await conn.execute("INSERT INTO sessions VALUES ($1, $2, $3);", session_token, user.id, expires)

    return Session(
        token=session_token,
        user=user.api_ready,
        expires=expires.isoformat(),
    )

@router.get("/{session_token}", response_model=Session, include_in_schema=False)
async def get_session(session_token: str, request: Request) -> Session:
    """Get a session by its token."""

    pass
