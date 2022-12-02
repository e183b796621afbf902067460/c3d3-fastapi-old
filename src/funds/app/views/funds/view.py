from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.funds.app import schemas
from src.funds.app.services.funds.service import FundService


router = InferringRouter()


@cbv(router=router)
class FundCBV:

    @router.post(
        "/sign-up",
        response_model=schemas.funds.TokenSchema,
        status_code=status.HTTP_201_CREATED
    )
    def on_post__label_sign_up(self, fund_create_schema: schemas.funds.FundCreateSchema, service: FundService = Depends()):
        return service.on_post__label_sign_up(fund_create_schema=fund_create_schema)

    @router.post(
        "/sign-in",
        response_model=schemas.funds.TokenSchema,
        status_code=status.HTTP_200_OK,
    )
    def on_post__label_sign_in(self, oauth2_: OAuth2PasswordRequestForm = Depends(), service: FundService = Depends()):
        return service.on_post__label_sign_in(oauth2_=oauth2_)

    @router.get(
        "/account",
        response_model=schemas.funds.FundORMSerializeSchema
    )
    def on_get__label_account(self, fund: schemas.funds.FundORMSerializeSchema = Depends(FundService.get_user_by_jwt_token)):
        return fund
