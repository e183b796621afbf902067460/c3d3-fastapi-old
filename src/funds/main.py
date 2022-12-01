from fastapi import FastAPI
import uvicorn
from src.funds.app.views.funds.view import router


app: FastAPI = FastAPI()

app.include_router(router)

uvicorn.run(app)
