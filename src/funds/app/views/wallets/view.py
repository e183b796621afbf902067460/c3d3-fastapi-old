from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status

from src.funds.app import schemas
from src.funds.app.services.wallets.service import WalletService


router = InferringRouter()


@cbv(router=router)
class WalletCBV:
    pass
