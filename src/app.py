from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.cfg.settings import settings
from src.funds.app.router import router as funds_flow_router


app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1}/openapi.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
def redirect(*args, **kwargs):
    return RedirectResponse(url=f'{settings.API_V1}/funds/labels/sign-in')


app.include_router(funds_flow_router, prefix=settings.API_V1)
