from fastapi import FastAPI, status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.services.service import C3Service
from app.schemas.schema import (
    LabelORMSchema, ExchangeSymbolLabelORMSchema, ExchangeTickerLabelORMSchema, ExchangeTickerORMSchema,
    NewLabelSchema, NewAccountLimitOrderSchema, NewAccountBalanceSchema,
    NewAccountLiquidationSchema, NewWholeMarketTradesHistory
)


app = FastAPI()
router = InferringRouter()


@cbv(router=router)
class C3CBV:

    @router.post(path='/new_account', status_code=status.HTTP_201_CREATED, response_model=LabelORMSchema)
    async def on_post__new_account(self, form: NewLabelSchema, service: C3Service = Depends()):
        new_account = service.on_post__new_account(
            label_name=form.label_name,
            label_api_key=form.label_api_key,
            label_api_secret=form.label_api_secret
        )
        return new_account

    @router.post(path='/new_account_balances', status_code=status.HTTP_201_CREATED, response_model=ExchangeSymbolLabelORMSchema)
    async def on_post__new_account_balances(self, form: NewAccountBalanceSchema, service: C3Service = Depends()):
        new_account_balances = service.on_post__new_account_balances(
            label_name=form.label_name,
            exchange_name=form.exchange_name,
            symbol_name=form.instrument_name
        )
        if not new_account_balances:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )
        return new_account_balances

    @router.post(path='/new_account_limit_orders', status_code=status.HTTP_201_CREATED, response_model=ExchangeTickerLabelORMSchema)
    async def on_post__new_account_limit_orders(self, form: NewAccountLimitOrderSchema, service: C3Service = Depends()):
        new_account_limit_orders = service.on_post__new_account_limit_orders(
            label_name=form.label_name,
            exchange_name=form.exchange_name,
            ticker_name=form.instrument_name
        )
        if not new_account_limit_orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )
        return new_account_limit_orders

    @router.post(path='/new_account_liquidations', status_code=status.HTTP_201_CREATED, response_model=ExchangeTickerLabelORMSchema)
    async def on_post__new_account_liquidations(self, form: NewAccountLiquidationSchema, service: C3Service = Depends()):
        new_account_liquidations = service.on_post__new_account_liquidations(
            label_name=form.label_name,
            exchange_name=form.exchange_name,
            ticker_name=form.instrument_name
        )
        if not new_account_liquidations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found."
            )
        return new_account_liquidations

    @router.post(path='/new_whole_market_trades_history', status_code=status.HTTP_201_CREATED, response_model=ExchangeTickerORMSchema)
    async def on_post__new_whole_market_trades_history(self, form: NewWholeMarketTradesHistory, service: C3Service = Depends()):
        new_whole_market_trades_history = service.on_post__new_whole_market_trades_history(
            exchange_name=form.exchange_name,
            ticker_name=form.instrument_name
        )
        return new_whole_market_trades_history


app.include_router(router=router, prefix=f'{settings.API_V1}' + '/c3')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')
