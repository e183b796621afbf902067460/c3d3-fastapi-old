from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status, HTTPException

from typing import List

from src.funds.app import schemas
from src.funds.app.services.wallets.service import WalletService
from src.funds.app.services.labels.service import current_label


router = InferringRouter()


@cbv(router=router)
class WalletCBV:

    @router.get(
        '/all',
        response_model=List[schemas.wallets.WalletORMSchema],
        status_code=status.HTTP_200_OK
    )
    def on_get__wallets_all(self, label: schemas.labels.LabelORMSchema = Depends(current_label), service: WalletService = Depends()):
        return service.on_get__wallets_all(label=label.h_label_name)

    @router.post(
        '/add',
        response_model=schemas.wallets.WalletORMSchema,
        status_code=status.HTTP_201_CREATED
    )
    def on_post__wallets_add(self, wallet_add_schema: schemas.wallets.WalletAddSchema, label: schemas.labels.LabelORMSchema = Depends(current_label), service: WalletService = Depends()):
        wallet: schemas.wallets.WalletORMSchema = service.on_post__wallets_add(
            address=wallet_add_schema.address,
            chain=wallet_add_schema.chain,
            label=label.h_label_name
        )
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Failed parameters'
            )
        return wallet

    @router.get(
        '/{wallet_address}',
        status_code=status.HTTP_200_OK,
        response_model=schemas.wallets.WalletORMSchema
    )
    def on_get__wallets_fetchone(self, wallet_address: str, service: WalletService = Depends(), label: schemas.labels.LabelORMSchema = Depends(current_label)):
        ...
