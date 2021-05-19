from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI

if not getenv("USE_DOCKER_ENV"):
    load_dotenv()

from src.routers import router
from src.utils.database import Database


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(router)

db = Database()

@app.on_event("startup")
async def on_startup() -> None:
    """Initialise the database."""

    await db.ainit()
