from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, status, HTTPException
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
        label = service.on_post__label_sign_in(label=oauth2_.username, password=oauth2_.password)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect label or password'
            )
        return {
            'access_token': service.create_access_token(id_=label.h_label_id),
            'refresh_token': service.create_refresh_token(id_=label.h_label_id)
        }

    @router.get(
        "/account",
        response_model=schemas.labels.LabelORMSerializeSchema
    )
    def on_get__label_account(self, fund: schemas.labels.LabelORMSerializeSchema = Depends(LabelService.get_user_by_jwt_token)):
        return fund
