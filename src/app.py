from fastapi import FastAPI

from src.funds.app.views.funds.view import router as funds_router


app: FastAPI = FastAPI(openapi_url='/auth/sign-in')

app.include_router(funds_router, prefix='/auth', tags=['Auth'])
