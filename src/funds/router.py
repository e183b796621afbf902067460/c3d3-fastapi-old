from fastapi import APIRouter

from src.funds.app.views.labels.view import router as funds_router
from src.funds.app.views.wallets.view import router as wallets_router


router = APIRouter(
    prefix='/funds'
)

router.include_router(funds_router, prefix='/labels', tags=['auth'])
router.include_router(wallets_router, prefix='/wallets', tags=['wallets'])
