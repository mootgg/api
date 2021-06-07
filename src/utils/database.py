from os import getenv, walk
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

        await self.automigrate()

    async def automigrate(self):
        allow = getenv("AUTOMIGRATE", "true")

        if allow != "true":
            return

        try:
            migration = await self.fetchrow("SELECT id FROM Migrations ORDER BY id DESC LIMIT 1;")
        except Exception as e:
            migration = None

        migration = migration["id"] if migration else 0

        fs = []

        for _root, _dirs, files in walk("./src/data/"):
            for file in files:
                mnum = int(file[0:4])
                fs.append((mnum, file))

        fs.sort()
        fs = [f for f in fs if f[0] > migration]

        if not fs:
            return

        for file in fs:
            res = await self.run_migration(file[1], file[0])
            if not res:
                break

    async def create_moot(self, id: int, content: str, user: m.User) -> m.Moot:
        """Create a new Moot."""

        async with self.pool.acquire() as conn:
            moot = await conn.fetchrow("INSERT INTO moots (id, content, author_id) VALUES ($1, $2, $3) RETURNING *;", id, content, user.id)

        return m.Moot(
            id=moot["id"],
            author=user,
            content=moot["content"],
            hide=moot["hide"],
            flags=moot["flags"],
        )

    async def get_moot(self, id: int) -> Optional[m.Moot]:
        """Get a Moot by ID."""

        async with self.pool.acquire() as conn:
            moot = await conn.fetchrow("SELECT * FROM moots WHERE id = $1;", id)
            if not moot:
                return None
            user = await conn.fetchrow("SELECT * FROM users WHERE id = $1;", moot["author_id"])

        return m.Moot(
            id=moot["id"],
            author=m.User(**dict(user)),
            content=moot["content"],
            hide=moot["hide"],
            flags=moot["flags"],
        )

    async def delete_moot(self, id: int) -> None:
        """Delete a Moot by ID."""

        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM moots WHERE id = $1;", id)

    async def create_user(self, id: int, discord_id: int, username: str, avatar_hash: str) -> m.User:
        """Create a new user."""

        async with self.pool.acquire() as conn:
            user = await conn.fetchrow(
                "INSERT INTO users (id, discord_id, username, avatar_hash) VALUES ($1, $2, $3, $4) RETURNING *;",
                id, discord_id, username, avatar_hash
            )

        return m.User(**dict(user))

    async def get_user(self, id: int) -> Optional[m.User]:
        """Get a user by ID."""

        async with self.pool.acquire() as conn:
            user = await conn.fetchrow("SELECT * FROM users WHERE id = $1;", id)

            if not user:
                return None

        return m.User(**dict(user))

    async def delete_user(self, id: int) -> None:
        """Delete a user by ID."""

        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM users WHERE id = $1;", id)
