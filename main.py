from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI


if not getenv("USE_DOCKER_ENV"):
    load_dotenv()

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
