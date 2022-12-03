from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.funds.app import schemas
from src.funds.app.services.labels.service import LabelService


router = InferringRouter()


@cbv(router=router)
class LabelCBV:

    @router.post(
        "/sign-up",
        response_model=schemas.labels.TokenSchema,
        status_code=status.HTTP_201_CREATED
    )
    def on_post__label_sign_up(self, fund_create_schema: schemas.labels.LabelCreateSchema, service: LabelService = Depends()):
        return service.on_post__label_sign_up(fund_create_schema=fund_create_schema)

    @router.post(
        "/sign-in",
        response_model=schemas.labels.TokenSchema,
        status_code=status.HTTP_200_OK,
    )
    def on_post__label_sign_in(self, oauth2_: OAuth2PasswordRequestForm = Depends(), service: LabelService = Depends()):
        return service.on_post__label_sign_in(oauth2_=oauth2_)

    @router.get(
        "/account",
        response_model=schemas.labels.LabelORMSerializeSchema
    )
    def on_get__label_account(self, fund: schemas.labels.LabelORMSerializeSchema = Depends(LabelService.get_user_by_jwt_token)):
        return fund

    @router.get(
        '/sign-in',
        status_code=status.HTTP_200_OK
    )
    def on_get__label_sign_in(self, request: Request, service: LabelService = Depends()):
        pass
