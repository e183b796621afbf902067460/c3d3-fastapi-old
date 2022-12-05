from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from passlib.context import CryptContext
import datetime
from datetime import timedelta
from typing import Optional

from src.funds.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.funds.orm import base
from src.funds.app import schemas


oauth2: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1}/funds/labels/sign-in')


class LabelService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
        self._crypto: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def _get_label_by_name(self, label: str) -> Optional[base.HubLabels]:
        return self._session.query(base.HubLabels).filter_by(h_label_name=label).first()

    def _hash_password(self, plain_password: str) -> str:
        return self._crypto.hash(secret=plain_password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._crypto.verify(secret=plain_password, hash=hashed_password)

    @staticmethod
    def _create_token(id_: int, expire: int, secret: str) -> str:
        expire_delta = datetime.datetime.utcnow() + timedelta(minutes=expire)
        payload = {
            'exp': expire_delta,
            'sub': str(id_)
        }
        return jwt.encode(payload, secret, settings.JWT_ALGORITHM)

    def create_access_token(self, id_: int) -> str:
        return self._create_token(
            id_=id_,
            expire=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            secret=settings.JWT_SECRET_KEY
        )

    def create_refresh_token(self, id_: int) -> str:
        return self._create_token(
            id_=id_,
            expire=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES,
            secret=settings.JWT_REFRESH_SECRET_KEY
        )

    def on_post__label_sign_in(self, label: str, password: str) -> Optional[schemas.labels.LabelORMSchema]:
        h_label: base.HubLabels = self._get_label_by_name(label=label)
        if not h_label:
            return None
        if not self._verify_password(plain_password=password, hashed_password=h_label.h_label_password):
            return None
        return schemas.labels.LabelORMSchema.from_orm(h_label)

