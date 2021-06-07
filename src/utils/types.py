from fastapi import Request as _BaseRequest

from src.utils.database import Database
from src.utils.ids import IDGenerator


class RequestState:
    db: Database
    ids: IDGenerator


class Request(_BaseRequest):
    state: RequestState
