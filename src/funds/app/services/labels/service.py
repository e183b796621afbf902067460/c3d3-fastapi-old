from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from passlib.hash import bcrypt
import datetime
from datetime import timedelta

from src.funds.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.funds.orm import base
from src.funds.app import schemas


oauth2: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='/sign-in')


class LabelService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session

    @staticmethod
    def _hash_password(plain_password: str) -> str:
        return bcrypt.hash(secret=plain_password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(secret=plain_password, hash=hashed_password)

    @staticmethod
    def _create_jwt_token(h_label: base.HubLabels) -> schemas.labels.TokenSchema:
        h_label_schema = schemas.labels.LabelORMDeserializeSchema.from_orm(h_label)
        utcnow = datetime.datetime.utcnow()
        payload = {
            'iat': utcnow,
            'nbf': utcnow,
            'exp': utcnow + timedelta(seconds=settings.JWT_EXPIRES),
            'sub': str(h_label_schema.h_label_id),
            'user': h_label_schema.dict(),
        }
        jwt_token = jwt.encode(
            claims=payload,
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        return schemas.labels.TokenSchema(access_token=jwt_token)

    @staticmethod
    def _verify_jwt_token(jwt_token: str) -> schemas.labels.LabelORMSerializeSchema:
        try:
            payload = jwt.decode(
                token=jwt_token,
                key=settings.JWT_SECRET,
                algorithms=[
                    settings.JWT_ALGORITHM
                ]
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Unverified JWT credentials',
                headers={
                    'WWW-Authenticate': 'Bearer'
                }
            )
        try:
            fund = schemas.labels.LabelORMSerializeSchema.parse_obj(payload.get('user'))
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Unverified credentials'
            )
        return fund

    def _get_user_by_username(self, username: str) -> base.HubLabels:
        return self._session.query(base.HubLabels).filter_by(h_label_name=username).first()

    @classmethod
    def get_user_by_jwt_token(cls, jwt_token: str = Depends(oauth2)) -> schemas.labels.LabelORMSerializeSchema:
        return cls._verify_jwt_token(jwt_token=jwt_token)

    def on_post__label_sign_up(self, fund_create_schema: schemas.labels.LabelCreateSchema) -> schemas.labels.TokenSchema:
        h_label: base.HubLabels = base.HubLabels(
            h_label_name=fund_create_schema.username,
            h_label_password=self._hash_password(
                plain_password=fund_create_schema.password
            )
        )
        if self._get_user_by_username(username=fund_create_schema.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Fund already registered, try to sign-in'
            )
        self._session.add(instance=h_label)
        self._session.commit()
        return self._create_jwt_token(h_label=h_label)

    def on_post__label_sign_in(self, oauth2_: OAuth2PasswordRequestForm) -> schemas.labels.TokenSchema:
        h_label: base.HubLabels = self._get_user_by_username(
            username=oauth2_.username
        )
        if not h_label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incorrect fund's label"
            )
        if not self._verify_password(
            plain_password=oauth2_.password,
            hashed_password=h_label.h_label_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect fund's password"
            )
        return self._create_jwt_token(h_label=h_label)

    def on_get__label_sign_in(self, request: Request):
        pass
