import jwt
from datetime import datetime, timedelta
from typing import Dict, Any

from app.cfg.settings import settings


class SecurityService:

    @staticmethod
    def access_token(data: dict) -> dict:
        def generate_token(
                data: dict,
                delta: timedelta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        ):
            return jwt.encode(
                payload={
                    'id': data['h_session_id'],
                    'exp': datetime.utcnow() + delta
                },
                key=settings.JWT_FERNET_KEY,
                algorithm=settings.JWT_ALGORITHM
            )
        return {
            'access_token': generate_token(data=data),
            'token_type': 'bearer'
        }

    @staticmethod
    def decode_token(authorization: str = None) -> Dict[str, Any]:
        if not authorization:
            raise PermissionError('Access Token is missing in header')

        return jwt.decode(
            jwt=authorization.replace('Bearer ', ''),
            key=settings.JWT_FERNET_KEY,
            algorithms=settings.JWT_ALGORITHM
        )

    @staticmethod
    def generate_header(token_payload: Dict[str, Any]) -> dict:
        return {
            'request-user-id': str(token_payload['id'])
        }
