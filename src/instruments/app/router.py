from fastapi import APIRouter

from src.instruments.app.views.pools.view import router as pools_router
from src.instruments.app.views.allocations.view import router as allocations_router


router = APIRouter(
    prefix='/instruments'
)

router.include_router(pools_router, prefix='/pools', tags=['pools'])
router.include_router(allocations_router, prefix='/allocations', tags=['allocations'])
