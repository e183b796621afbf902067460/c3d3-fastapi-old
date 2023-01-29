from fastapi import FastAPI, status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.services.service import D3Service
from app.schemas.schema import (
    TokenOnWalletORMSchema, ChainORMSchema,
    AddressChainProtocolSpecificationORMSchema,
    AddressChainProtocolSpecificationLabelORMSchema,
    NewChainSchema, NewBidsAndAsksSchema,
    NewHedgeToBorrowsSchema, NewHedgeToSuppliesSchema,
    NewWalletBalancesSchema
)


app = FastAPI()
router = InferringRouter()


@cbv(router=router)
class D3CBV:

    @router.post(path='/new_chain', status_code=status.HTTP_201_CREATED, response_model=ChainORMSchema)
    async def on_post__new_chain(self, form: NewChainSchema, service: D3Service = Depends()):
        new_chain = service.on_post__new_chain(
            network_name=form.network_name,
            native_chain_token=form.native_chain_token,
            rpc_node=form.rpc_node,
            block_limit=form.block_limit,
            network_uri=form.network_uri,
            network_api_key=form.network_api_key
        )
        return new_chain

    @router.post(path='/new_bids_and_asks', status_code=status.HTTP_201_CREATED, response_model=AddressChainProtocolSpecificationORMSchema)
    async def on_post__new_bids_and_asks(self, form: NewBidsAndAsksSchema, service: D3Service = Depends()):
        new_bids_and_asks = service.on_post__new_bids_and_asks(
            pool_address=form.pool_address,
            network_name=form.network_name,
            protocol_name=form.specification_name,
            specification_name=form.specification_name,
            is_reverse=form.is_reverse
        )
        if not new_bids_and_asks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chain not found."
            )
        return new_bids_and_asks

    @router.post(path='/new_hedge_to_borrows', status_code=status.HTTP_201_CREATED, response_model=AddressChainProtocolSpecificationLabelORMSchema)
    async def on_post__new_hedge_to_borrows(self, form: NewHedgeToBorrowsSchema, service: D3Service = Depends()):
        new_hedge_to_borrows = service.on_post__new_hedge_to_borrows(
            wallet_address=form.wallet_address,
            token_address=form.token_address,
            network_name=form.network_name,
            label_name=form.label_name,
            protocol_name=form.protocol_name,
            specification_name=form.specification_name
        )
        if not new_hedge_to_borrows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chain not found."
            )
        return new_hedge_to_borrows

    @router.post(path='/new_hedge_to_supplies', status_code=status.HTTP_201_CREATED, response_model=AddressChainProtocolSpecificationLabelORMSchema)
    async def on_post__new_hedge_to_supplies(self, form: NewHedgeToSuppliesSchema, service: D3Service = Depends()):
        new_hedge_to_supplies = service.on_post__new_hedge_to_supplies(
            wallet_address=form.wallet_address,
            token_address=form.token_address,
            network_name=form.network_name,
            label_name=form.label_name,
            protocol_name=form.protocol_name,
            specification_name=form.specification_name
        )
        if not new_hedge_to_supplies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chain not found."
            )
        return new_hedge_to_supplies

    @router.post(path='/new_wallet_balances', status_code=status.HTTP_201_CREATED, response_model=TokenOnWalletORMSchema)
    async def on_post__new_wallet_balances(self, form: NewWalletBalancesSchema, service: D3Service = Depends()):
        new_wallet_balances = service.on_post__new_wallet_balances(
            wallet_address=form.wallet_address,
            token_address=form.token_address,
            network_name=form.network_name,
            label_name=form.label_name
        )
        if not new_wallet_balances:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chain not found."
            )
        return new_wallet_balances


app.include_router(router=router, prefix=f'{settings.API_V1}' + '/d3')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')
