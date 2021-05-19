from fastapi import APIRouter, Request

from src.models.api import User, NewUser


router = APIRouter(prefix="/users")

@router.post("/", response_model=User, include_in_schema=False)
async def new_user(data: NewUser, request: Request) -> User:
    """Create a new user."""

    request.state.auth.raise_for_internal()
