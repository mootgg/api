from os import getenv

from aiohttp import ClientSession
from aioredis import create_redis_pool
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

if not getenv("USE_DOCKER_ENV"):
    load_dotenv()

from src.routers import router
from src.utils.auth import authenticate as auth
from src.utils.database import Database
from src.utils.ids import IDGenerator

app = FastAPI(docs_url=None, redoc_url="/developers")
app.include_router(router)

db = Database()
ids = IDGenerator()
sess = ClientSession()
redis = None


@app.on_event("startup")
async def on_startup() -> None:
    """Initialise the database."""

    await db.ainit()

    global redis
    redis = await create_redis_pool(address="redis://127.0.0.1")


@app.middleware("http")
async def authenticate(request: Request, call_next) -> Response:
    """Authenticate all requests."""

    request.state.auth = await auth(request, db)
    request.state.db = db
    request.state.ids = ids
    request.state.sess = sess
    request.state.redis = redis

    return await call_next(request)
