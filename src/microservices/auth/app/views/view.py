from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.services.service import SessionService
from app.schemas.schema import SessionLoginSchema


app = FastAPI()
router = InferringRouter()


@cbv(router=router)
class AuthCBV:

    @router.post(path=f'{settings.API_V1}/login', status_code=status.HTTP_200_OK)
    async def on_post__login(self, form: SessionLoginSchema, service: SessionService = Depends()):
        session = service.on_post__login(session_name=form.username, password=form.password)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Incorrect credentials.'
            )
        return session


app.include_router(router=router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')
