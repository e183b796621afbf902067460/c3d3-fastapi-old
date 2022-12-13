from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from web3 import Web3

from typing import List, Optional

from src.instruments.app import schemas
from src.funds.app import schemas as funds_schemas
from src.instruments.app.services.pools.service import PoolService
from src.funds.app.services.labels.service import current_label
from src.cfg.settings import settings


router = InferringRouter()


@cbv(router=router)
class PoolCBV:

    @router.post(
        '/{network_name}/{wallet_address}',
        response_model=schemas.pools.PoolORMSchema,
        status_code=status.HTTP_201_CREATED
    )
    def on_post__pools_add_pool(self, network_name: str, wallet_address: str, pool_add_schema: schemas.pools.PoolAddSchema, label: funds_schemas.labels.LabelORMSchema = Depends(current_label), service: PoolService = Depends()):
        if not Web3.isAddress(wallet_address) or not Web3.isAddress(pool_add_schema.address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid wallet or pool address'
            )
        pool: schemas.pools.PoolORMSchema = service.on_post__pools_add_pool(
            pool_address=Web3.toChecksumAddress(pool_add_schema.address),
            wallet_address=Web3.toChecksumAddress(wallet_address),
            chain=network_name.lower(),
            label=label.h_label_name,
            protocol=pool_add_schema.protocol.lower(),
            protocol_category=pool_add_schema.protocol_category.lower(),
            pool_name=pool_add_schema.pool_name
        )
        if not pool:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed parameters'
            )
        return pool

    @router.delete(
        '/{network_name}/{wallet_address}/{protocol}/{protocol_category}/{address}/{pool_name}',
        status_code=status.HTTP_202_ACCEPTED,
        response_model=schemas.pools.PoolDeleteSchema
    )
    def on_delete__pools_delete_pool(
            self,
            wallet_address: str,
            network_name: str,
            protocol: str,
            protocol_category: str,
            address: str,
            pool_name: str,
            service: PoolService = Depends(),
            label: funds_schemas.labels.LabelORMSchema = Depends(current_label)
    ):
        if not Web3.isAddress(wallet_address) or not Web3.isAddress(address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid wallet or pool address'
            )
        is_delete: bool = service.on_delete__pools_delete_pool(
            pool_address=Web3.toChecksumAddress(address),
            protocol=protocol.lower(),
            protocol_category=protocol_category.lower(),
            chain=network_name.lower(),
            wallet_address=Web3.toChecksumAddress(wallet_address),
            label_id=label.h_label_id
        )
        if is_delete:
            return schemas.pools.PoolDeleteSchema(
                address=Web3.toChecksumAddress(address),
                protocol=protocol.lower(),
                protocol_category=protocol_category.lower(),
                pool_name=pool_name.lower()
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pool doesn't exist"
        )


