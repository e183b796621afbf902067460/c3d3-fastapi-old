from fastapi import FastAPI
from funds.app.views.labels.view import router


app: FastAPI = FastAPI()

app.include_router(router)
