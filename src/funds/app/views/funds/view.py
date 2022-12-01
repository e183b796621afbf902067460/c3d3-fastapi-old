from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from src.funds.orm.cfg.engine import settings
from src.funds.app.services.funds.service import LabelBase
from src.funds.app.forms.funds.forms import LabelForm


router = InferringRouter()


@cbv(router=router)
class LabelCBV(LabelBase):
    _session = Depends(settings.get_session)

    @router.post("/sign-up")
    def on_post__label_sign_up(self, label: LabelForm):
        db_label = self._get_label_by_name(label=label.name)
        if db_label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Label already registered, try to sign-in'
            )
        model = self._create_label(label=label)

        return RedirectResponse(
            f'/account/{model.h_label_name}',
            status_code=status.HTTP_302_FOUND
        )

    @router.post("/sign-in")
    def on_post__label_sign_in(self, label: LabelForm):
        db_label = self._get_label_by_name(label=label.name)
        if not db_label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Label is not registered, try to sign-up'
            )
        if not self._validate_password(password=label.password, hashed_password=db_label.h_label_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Wrong password, try again'
            )
        return RedirectResponse(
            f'/account/{db_label.h_label_name}',
            status_code=status.HTTP_302_FOUND
        )

    @router.get("/account/{label}")
    def on_get__label_account(self, label: str):
        db_label = self._get_label_by_name(label=label)
        if not db_label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Inactive token'
            )
        return db_label
