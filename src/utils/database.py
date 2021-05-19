from os import getenv
from typing import Optional

from asyncpg import create_pool, Pool

from src.models import database as m


class Database:
    """A database class to aid making requests."""

    def __init__(self) -> None:
        self.pool: Pool = None

    async def ainit(self) -> None:
        """Asynchronously initialize the database."""

        self.pool = await create_pool(getenv("DB_DSN"))

    async def get_moot(self, id: int) -> Optional[m.Moot]:
        """Get a Moot by ID."""

        async with self.pool.acquire() as conn:
            moot = await conn.fetchrow("SELECT * FROM Moots WHERE id = $1;", id)
            if not moot:
                return None
            user = await conn.fetchrow("SELECT * FROM Users WHERE id = $1;", moot["author_id"])

        return m.Moot(
            id=moot["id"],
            author=m.User(**dict(user)),
            content=moot["content"],
            hide=moot["hide"],
            flags=moot["flags"],
        )
