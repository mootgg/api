from dataclasses import dataclass


@dataclass
class User:
    id: int
    discord_id: int
    username: str
    avatar_hash: str
    bio: str
    banned: bool
    flags: int


@dataclass
class Auth:
    token: str
    user: User
    perms: int
