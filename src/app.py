from fastapi import FastAPI

from src.funds.app.views.funds.view import router


app: FastAPI = FastAPI()

app.include_router(router, prefix='/auth', tags=['Auth'])
