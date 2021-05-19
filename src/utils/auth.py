from dataclasses import dataclass
from os import getenv

from fastapi import Request
from fastapi.exceptions import HTTPException

from src.models.database import User, Auth
from src.utils.database import Database
from src.utils.bitfield import BitField


INTERNAL_TOKEN = getenv('INTERNAL_TOKEN')


@dataclass
class AuthState:
    valid: bool
    internal: bool = False
    auth: Auth = None

    def raise_for_validity(self) -> None:
        if not self.valid:
            raise HTTPException(401, "Invalid token.")

    def raise_for_internal(self) -> None:
        if not self.internal:
            raise HTTPException(403, "Access denied: Internal endpoint.")

    def raise_for_access(self, resource: int) -> bool:
        if not BitField(self.auth.perms)[resource]:
            raise HTTPException(403, "Access denied: Bad resource.")


async def authenticate(request: Request, database: Database) -> AuthState:
    """Authenticate a request.

    Args:
        request (Request): The request to authenticate.
        database (Database): The database to use for authentication.

    Returns:
        AuthState: The resulting authentication state.
    """

    token = request.headers.get("Authorization", None)

    if not token:
        return AuthState(valid=False)

    if token == INTERNAL_TOKEN:
        return AuthState(valid=True, internal=True)

    async with database.pool.acquire() as conn:
        access = await conn.fetchrow("SELECT * FROM api_keys INNER JOIN users ON (api_keys.parent_id = users.id) WHERE api_keys.token = $1;", token)

    if not access:
        return AuthState(valid=False)

    user = User(
        id=access["id"],
        discord_id=access["discord_id"],
        username=access["username"],
        avatar_hash=access["avatar_hash"],
        bio=access["bio"],
        banned=access["banned"],
        flags=access["flags"],
    )
    state = Auth(
        token=access["token"],
        user=user,
        perms=access["perms"],
    )

    return AuthState(valid=True, auth=state)
