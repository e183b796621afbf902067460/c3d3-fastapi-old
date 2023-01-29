from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import APIRouter, InferringRouter

from app.cfg.settings import settings
from app.schemas.d3.schema import (
    NewHedgeToSuppliesSchema, NewHedgeToBorrowsSchema,
    NewWalletBalancesSchema, NewChainSchema, NewBidsAndAsksSchema,
    ChainORMSchema, TokenOnWalletORMSchema, AddressChainProtocolSpecificationLabelORMSchema,
    AddressChainProtocolSpecificationORMSchema
)
from app.services.router.service import RouterService as gateway


app = APIRouter()
router = InferringRouter()


@cbv(router=router)
class D3CBV:

    @gateway.route(
        method=router.post,
        path='/new_chain',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_chain',
        service_url=settings.D3_SERVICE_URL,
        response_model=ChainORMSchema,
        is_permission=True
    )
    async def on_post__new_chain(self, request: Request, response: Response, new_chain: NewChainSchema):
        pass

    @gateway.route(
        method=router.post,
        path='/new_bids_and_asks',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_bids_and_asks',
        service_url=settings.D3_SERVICE_URL,
        response_model=AddressChainProtocolSpecificationORMSchema,
        is_permission=True
    )
    async def on_post__new_bids_and_asks(self, request: Request, response: Response, new_bids_and_asks: NewBidsAndAsksSchema):
        pass

    @gateway.route(
        method=router.post,
        path='/new_hedge_to_borrows',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_hedge_to_borrows',
        service_url=settings.D3_SERVICE_URL,
        response_model=AddressChainProtocolSpecificationLabelORMSchema,
        is_permission=True
    )
    async def on_post__new_hedge_to_borrows(self, request: Request, response: Response, new_hedge_to_borrows: NewHedgeToBorrowsSchema):
        pass

    @gateway.route(
        method=router.post,
        path='/new_hedge_to_supplies',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_hedge_to_supplies',
        service_url=settings.D3_SERVICE_URL,
        response_model=AddressChainProtocolSpecificationLabelORMSchema,
        is_permission=True
    )
    async def on_post__new_hedge_to_supplies(self, request: Request, response: Response, new_hedge_to_supplies: NewHedgeToSuppliesSchema):
        pass

    @gateway.route(
        method=router.post,
        path='/new_wallet_balances',
        status_code=status.HTTP_201_CREATED,
        payload_key='new_wallet_balances',
        service_url=settings.D3_SERVICE_URL,
        response_model=TokenOnWalletORMSchema,
        is_permission=True
    )
    async def on_post__new_wallet_balances(self, request: Request, response: Response, new_wallet_balances: NewWalletBalancesSchema):
        pass


app.include_router(router=router, prefix=f'{settings.API_V1}' + '/d3')
