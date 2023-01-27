from fastapi import status, Request, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import APIRouter, InferringRouter

from app.cfg.settings import settings
from app.schemas.auth.schema import LoginResponseSchema, SessionLoginSchema
from app.services.router.service import RouterService as gateway


app = APIRouter()
router = InferringRouter()


@cbv(router=router)
class AuthCBV:

    @gateway.route(
        method=router.post,
        path=f'{settings.API_V1}/login',
        status_code=status.HTTP_200_OK,
        payload_key='oauth2',
        service_url=settings.AUTH_SERVICE_URL,
        response_model=LoginResponseSchema,
        is_access_token=True
    )
    async def on_post__login(self, request: Request, response: Response, oauth2: SessionLoginSchema):
        pass


app.include_router(router=router)
