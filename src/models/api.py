from pydantic import BaseModel, constr


class User(BaseModel):
    id: int
    username: str
    avatar: str
    flags: int


class Moot(BaseModel):
    id: int
    content: str
    hidden: bool
    flags: int
    author: User


class NewMoot(BaseModel):
    content: constr(min_length=280, max_length=65536)
