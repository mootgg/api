from datetime import datetime, timedelta
from os import getenv
from random import randrange
from secrets import token_hex

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.models.api import Session
from src.utils.types import Request
from starlette_discord import DiscordOAuthClient

router = APIRouter(prefix="/sessions")
discord = DiscordOAuthClient(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"), "")


@router.post("/{token}", response_model=Session, include_in_schema=False)
async def new_session(token: str, request: Request) -> Session:
    """Create a new user session."""

    request.state.auth.raise_for_internal()
    raw_user = await discord.login(token)

    user = await request.state.db.get_user(int(raw_user["id"]))

    if not user:
        user = await request.state.db.create_user(
            request.state.ids.next(),
            int(raw_user["id"]),
            raw_user["username"]
            + "#"
            + raw_user["discriminator"]
            + str(randrange(1, 9999)).zfill(4),
            raw_user.get("avatar", None),
        )

    session_token = token_hex(64)
    expires = datetime.utcnow() + timedelta(days=7)

    async with request.state.db.pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO sessions VALUES ($1, $2, $3);", session_token, user.id, expires
        )

    return Session(
        token=session_token,
        user=user.api_ready,
        expires=expires.isoformat(),
    )


@router.get("/{session_token}", response_model=Session, include_in_schema=False)
async def get_session(session_token: str, request: Request) -> Session:
    """Get a session by its token."""

    request.state.auth.raise_for_internal()

    session = await request.state.db.fetchrow(
        "SELECT * FROM Sessions WHERE token = $1;", session_token
    )
    if not session:
        raise HTTPException(404)

    user = await request.state.db.get_user(session["parent_id"])

    return Session(
        token=session_token,
        user=user.api_ready,
        expires=session["expires"].isoformat(),
    )
