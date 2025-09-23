from fastapi import FastAPI
from .adapters.web import api

app = FastAPI()

app.include_router(api.router)
