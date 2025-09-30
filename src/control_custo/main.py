import logging

from fastapi import FastAPI
from .adapters.web import api


file_log = 'store/logs/app.log'

# Configuração básica de logging - DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(file_log, mode="a", encoding="utf-8"),
        logging.StreamHandler()  # imprime no console (stdout)
    ]
)

logger = logging.getLogger(__name__)
access_logger = logging.getLogger("uvicorn.access")  # acessos HTTP

app = FastAPI(root_path='/api')

app.include_router(api.router)
