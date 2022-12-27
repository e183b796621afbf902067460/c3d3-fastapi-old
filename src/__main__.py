import uvicorn

from src.app import app
from src.cfg.settings import settings


uvicorn.run(
    app=app,
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT
)
