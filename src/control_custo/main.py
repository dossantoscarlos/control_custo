from fastapi import FastAPI
from .adapters.web import api
import logging

app = FastAPI(root_path='/api')

logger = logging.getLogger("uvicorn.error")  # logger do servidor
access_logger = logging.getLogger("uvicorn.access")  # acessos HTTP

app.include_router(api.router)
