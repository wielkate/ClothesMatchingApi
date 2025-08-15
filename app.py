import logging

from fastapi import FastAPI

from v1 import app_v1

GREY_LIGHT = '\033[37m'
WHITE = '\033[97m'
GREEN = '\033[92m'
CYAN = '\033[36m'

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format=f'{CYAN}%(asctime)s  {GREY_LIGHT}%(name)s  {GREEN}[%(levelname)s]: {WHITE}%(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    summary="Internal API for managing clothes",
    version="1.0.0",
    title="Clothes Matcher API"
)
app.mount("/v1", app_v1)
