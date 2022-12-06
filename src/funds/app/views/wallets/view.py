from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status, HTTPException
from fastapi.responses import RedirectResponse

from typing import List, Optional

from src.funds.app import schemas
from src.funds.app.services.wallets.service import WalletService
from src.funds.app.services.labels.service import current_label
from src.cfg.settings import settings


router = InferringRouter()


@cbv(router=router)
class WalletCBV:

    @router.get(
        '/all',
        response_model=List[Optional[schemas.wallets.WalletORMSchema]],
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
        '/{wallet_id}',
        status_code=status.HTTP_200_OK,
        response_model=schemas.wallets.WalletORMSchema
    )
    def on_get__wallets_fetchone(self, wallet_id: int, service: WalletService = Depends(), label: schemas.labels.LabelORMSchema = Depends(current_label)):
        fund = service.on_get__wallets_fetchone(wallet_id=wallet_id, label_id=label.h_label_id)
        if not fund:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fund doesn't existed"
            )
        return fund

    @router.delete(
        '/{wallet_id}',
        status_code=status.HTTP_202_ACCEPTED,
        response_class=RedirectResponse
    )
    def on_delete__wallets_delete_fund(self, wallet_id: int, service: WalletService = Depends(), label: schemas.labels.LabelORMSchema = Depends(current_label)):
        is_delete: bool = service.on_delete__wallets_delete_fund(wallet_id=wallet_id, label_id=label.h_label_id)
        if is_delete:
            return f'{settings.API_V1}/funds/wallets/all'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund doesn't existed"
        )


