import uvicorn

from src.cfg.settings import settings
from src.app import app


uvicorn.run(
    app=app,
    host=settings.SERVER_HOST,
    port=settings.SERVER_PORT
)
