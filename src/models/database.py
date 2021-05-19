from dataclasses import dataclass

from .api import Moot as APIMoot, User as APIUser


@dataclass
class User:
    id: int
    discord_id: int
    username: str
    avatar_hash: str
    bio: str
    banned: bool
    flags: int

    @property
    def api_ready(self) -> APIUser:
        return APIUser(
            id=self.id,
            username=self.username,
            avatar=self.avatar_hash,
            flags=self.flags,
        )

@dataclass
class Auth:
    token: str
    user: User
    perms: int


@dataclass
class Moot:
    id: int
    author: User
    content: str
    hide: bool
    flags: int

    @property
    def api_ready(self) -> APIMoot:
        return APIMoot(
            id=self.id,
            content=self.content,
            hidden=self.hide,
            flags=self.flags,
            author=self.author.api_ready,
        )
