from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, HTTPException, status

from funds.orm.cfg.engine import settings
from funds.app.base.labels.base import LabelBase
from funds.app.forms.labels.forms import LabelForm


router = InferringRouter()


@cbv(router=router)
class LabelsCBV(LabelBase):
    _session = Depends(settings.get_session)

    @router.post("/sign-up")
    def on_post__label_sign_up(self, label: LabelForm) -> str:
        db_label = self._get_label_by_name(label=label.name)
        if db_label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Label already registered, try to sign-in'
            )
        return self._create_label(label=label)

    @router.post("/sign-in")
    def on_post__label_sign_in(self, label: LabelForm):
        db_label = self._get_label_by_name(label=label.name)
        if not db_label:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Label is not registered, try to sign-up'
            )
        ...
