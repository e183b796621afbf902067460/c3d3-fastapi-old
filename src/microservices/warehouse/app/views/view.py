from typing import Any
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.cfg.settings import settings
from app.services.service import WarehouseService


app = FastAPI()
router = InferringRouter()


@cbv(router=router)
class WarehouseCBV:

    @router.post(path='/query', status_code=status.HTTP_200_OK, response_model=Any)
    async def on_post__query(self, query: str, service: WarehouseService = Depends()):
        result = service.on_post__query(query=query)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Incorrect query.'
            )
        return result


app.include_router(router=router, prefix=f'{settings.API_V1}' + '/warehouse')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='view:app', host='0.0.0.0')
