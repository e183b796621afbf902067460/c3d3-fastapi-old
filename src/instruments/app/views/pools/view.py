from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status, HTTPException
from fastapi.responses import RedirectResponse

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
        pool: schemas.pools.PoolORMSchema = service.on_post__pools_add_pool(
            pool_address=pool_add_schema.address,
            wallet_address=wallet_address,
            chain=network_name,
            label=label.h_label_name,
            protocol=pool_add_schema.protocol,
            protocol_category=pool_add_schema.protocol_category
        )
        if not pool:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed parameters'
            )
        return pool

    @router.delete(
        '/{network_name}/{wallet_address}',
        status_code=status.HTTP_202_ACCEPTED,
        response_class=RedirectResponse
    )
    def on_delete__pools_delete_pool(self, wallet_address: str, network_name: str, pool_delete_schema: schemas.pools.PoolDeleteSchema, service: PoolService = Depends(), label: funds_schemas.labels.LabelORMSchema = Depends(current_label)):
        is_delete: bool = service.on_delete__pools_delete_pool(
            pool_address=pool_delete_schema.address,
            protocol=pool_delete_schema.protocol,
            protocol_category=pool_delete_schema.protocol_category,
            chain=network_name,
            wallet_address=wallet_address,
            label_id=label.h_label_id
        )
        if is_delete:
            return f'{settings.API_V1}/funds/wallets/all'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pool doesn't exist"
        )


