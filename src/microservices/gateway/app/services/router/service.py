import aiohttp
from functools import wraps
import async_timeout
from typing import Callable, Optional

from fastapi import Request, Response, HTTPException, status

from app.services.security.service import SecurityService
from app.cfg.settings import settings


class RouterService:

    security_service: SecurityService = SecurityService

    @staticmethod
    async def _r(
            url: str,
            method: str,
            data: dict = None,
            headers: dict = None
    ):
        data = data or dict()
        with async_timeout.timeout(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES):
            async with aiohttp.ClientSession() as session:
                request = getattr(session, method)
                async with request(url, json=data, headers=headers) as response:
                    data = await response.json()
                    return data, response.status

    @classmethod
    def route(
            cls,
            method: Callable,
            path: str,
            status_code: int,
            payload_key: str,
            service_url: str,
            response_model=None,
            is_permission: bool = False,
            is_access_token: Optional[bool] = None,
            is_header: bool = False
    ):

        method = method(
            path=path,
            status_code=status_code,
            response_model=response_model
        )

        def wrapper(fn):

            @method
            @wraps(fn)
            async def inner(
                    request: Request,
                    response: Response,
                    **kwargs
            ):
                if is_permission:
                    try:
                        payload = cls.security_service.decode_token(request.headers.get('authorization'))
                    except Exception as e:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=str(e),
                            headers={
                                'WWW-Authenticate': 'Bearer'
                            },
                        )
                try:
                    data, r_status_code = await cls._r(
                        url=f"{service_url}{request.scope['path']}",
                        method=request.scope['method'].lower(),
                        data=kwargs.get(payload_key).dict() if kwargs.get(payload_key) else dict(),
                        headers=dict() if not is_header else cls.security_service.generate_header(payload),
                    )
                except aiohttp.client.ClientConnectorError:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail='Service is unavailable',
                        headers={
                            'WWW-Authenticate': 'Bearer'
                        },
                    )
                except aiohttp.client.ContentTypeError:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Service error',
                        headers={
                            'WWW-Authenticate': 'Bearer'
                        },
                    )
                response.status_code = r_status_code
                return cls.security_service.access_token(data) if (r_status_code == status_code and is_access_token) else data
        return wrapper
