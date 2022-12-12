import uvicorn
from decouple import config

from src.app import app


uvicorn.run(
    app=app,
    host=config('SERVER_HOST', cast=str, default='127.0.0.0'),
    port=config('SERVER_PORT', cast=int, default=8000)
)
