from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from web3 import Web3

from typing import List, Optional

from src.instruments.app import schemas
from src.funds.app import schemas as funds_schemas
from src.instruments.app.services.allocations.service import AllocationService
from src.funds.app.services.labels.service import current_label
from src.cfg.settings import settings


router = InferringRouter()


@cbv(router=router)
class AllocationCBV:

    @router.post(
        '/{network_name}/{wallet_address}',
        response_model=schemas.allocations.AllocationORMSchema,
        status_code=status.HTTP_201_CREATED
    )
    def on_post__allocations_add_allocation(self, network_name: str, wallet_address: str, allocation_add_schema: schemas.allocations.AllocationAddSchema, label: funds_schemas.labels.LabelORMSchema = Depends(current_label), service: AllocationService = Depends()):
        if not Web3.isAddress(wallet_address) or not Web3.isAddress(allocation_add_schema.address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid wallet or pool address'
            )
        allocation: schemas.pools.PoolORMSchema = service.on_post__allocations_add_allocation(
            pool_address=Web3.toChecksumAddress(allocation_add_schema.address),
            wallet_address=Web3.toChecksumAddress(wallet_address),
            chain=network_name.lower(),
            label=label.h_label_name,
            protocol=allocation_add_schema.protocol.lower(),
            protocol_category=allocation_add_schema.protocol_category.lower(),
            pool_name=allocation_add_schema.pool_name
        )
        if not allocation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed parameters'
            )
        return allocation

    @router.delete(
        '/{network_name}/{wallet_address}/{protocol}/{protocol_category}/{address}/{pool_name}',
        status_code=status.HTTP_202_ACCEPTED,
        response_model=schemas.allocations.AllocationDeleteSchema
    )
    def on_delete__allocations_delete_allocation(
            self,
            wallet_address: str,
            network_name: str,
            protocol: str,
            protocol_category: str,
            address: str,
            pool_name: str,
            service: AllocationService = Depends(),
            label: funds_schemas.labels.LabelORMSchema = Depends(current_label)
    ):
        if not Web3.isAddress(wallet_address) or not Web3.isAddress(address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid wallet or pool address'
            )
        is_delete: bool = service.on_delete__allocations_delete_allocation(
            pool_address=Web3.toChecksumAddress(address),
            protocol=protocol.lower(),
            protocol_category=protocol_category.lower(),
            chain=network_name.lower(),
            wallet_address=Web3.toChecksumAddress(wallet_address),
            label_id=label.h_label_id
        )
        if is_delete:
            return schemas.allocations.AllocationDeleteSchema(
                address=Web3.toChecksumAddress(address),
                protocol=protocol.lower(),
                protocol_category=protocol_category.lower(),
                pool_name=pool_name.lower()
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allocation doesn't exist"
        )


