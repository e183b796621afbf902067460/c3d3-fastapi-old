from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import APIRouter, InferringRouter

from app.cfg.settings import settings
from app.schemas.c3.schema import (
    LabelORMSchema, ExchangeTickerORMSchema, ExchangeTickerLabelORMSchema, ExchangeSymbolLabelORMSchema,
    NewLabelSchema, NewAccountLiquidationSchema, NewAccountLimitOrderSchema, NewAccountBalanceSchema, NewWholeMarketTradesHistory
)
from app.services.router.service import RouterService as gateway


app = APIRouter()
router = InferringRouter()


@cbv(router=router)
class C3CBV:

    @gateway.route(
        method=router.post,
        path=f'{settings.API_V1}/new_account',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_account',
        service_url=settings.C3_SERVICE_URL,
        response_model=LabelORMSchema,
        is_permission=True
    )
    async def on_post__new_account(self, request: Request, response: Response, new_account: NewLabelSchema):
        pass

    @gateway.route(
        method=router.post,
        path=f'{settings.API_V1}/new_account_balances',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_account_balance',
        service_url=settings.C3_SERVICE_URL,
        response_model=ExchangeSymbolLabelORMSchema,
        is_permission=True
    )
    async def on_post__new_account_balances(self, request: Request, response: Response, new_account_balance: NewAccountBalanceSchema):
        pass

    @gateway.route(
        method=router.post,
        path=f'{settings.API_V1}/new_account_limit_orders',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_account_limit_order',
        service_url=settings.C3_SERVICE_URL,
        response_model=ExchangeTickerLabelORMSchema,
        is_permission=True
    )
    async def on_post__new_account_limit_orders(self, request: Request, response: Response, new_account_limit_orders: NewAccountLimitOrderSchema):
        pass

    @gateway.route(
        method=router.post,
        path=f'{settings.API_V1}/new_account_liquidations',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_account_liquidation',
        service_url=settings.C3_SERVICE_URL,
        response_model=ExchangeTickerLabelORMSchema,
        is_permission=True
    )
    async def on_post__new_account_liquidations(self, request: Request, response: Response, new_account_liquidation: NewAccountLiquidationSchema):
        pass

    @gateway.route(
        method=router.post,
        path=f'{settings.API_V1}/new_whole_market_trades_history',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_whole_market_trades_history',
        service_url=settings.C3_SERVICE_URL,
        response_model=ExchangeTickerORMSchema,
        is_permission=True
    )
    async def on_post__new_whole_market_trades_history(self, request: Request, response: Response, new_whole_market_trades_history: NewWholeMarketTradesHistory):
        pass


app.include_router(router=router)
