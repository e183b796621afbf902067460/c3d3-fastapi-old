from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status

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
