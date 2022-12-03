from fastapi import FastAPI, status
from starlette.responses import RedirectResponse

from src.funds.app.views.labels.view import router as funds_router
from src.funds.app.views.wallets.view import router as wallets_router


app: FastAPI = FastAPI()


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
def redirect(*args, **kwargs):
    return RedirectResponse(url='/funds/sign-in')


app.include_router(funds_router, prefix='/funds', tags=['Auth'])
app.include_router(wallets_router, prefix='/wallets', tags=['Wallets'])
