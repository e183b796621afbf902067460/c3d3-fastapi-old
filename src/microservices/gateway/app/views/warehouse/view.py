from typing import Any
from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import APIRouter, InferringRouter

from app.cfg.settings import settings
from app.services.router.service import RouterService as gateway


app = APIRouter()
router = InferringRouter()


@cbv(router=router)
class WarehouseCBV:

    @gateway.route(
        method=router.post,
        path='/query',
        status_code=status.HTTP_200_OK,
        payload_key='query',
        service_url=settings.WAREHOUSE_URL,
        response_model=Any,
        is_access_token=True
    )
    async def on_post__query(self, request: Request, response: Response, query: str):
        pass


app.include_router(router=router, prefix=f'{settings.API_V1}' + '/warehouse')
