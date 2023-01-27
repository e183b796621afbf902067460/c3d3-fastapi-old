from sqlalchemy.orm import Session
from fastapi import Depends
from passlib.context import CryptContext
from typing import Optional

from app.orm.cfg.engine import ORMSettings
from app.orm import base
from app.schemas.schema import SessionORMSchema


class SessionService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self.__session: Session = session
        self.__crypto: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.__crypto.verify(secret=plain_password, hash=hashed_password)

    def _get_session_by_name(self, session_name: str) -> Optional[base.hSessions]:
        return self.__session.query(base.hSessions).filter_by(h_session_name=session_name).first()

    def on_post__login(self, session_name: str, password: str) -> Optional[SessionORMSchema]:
        h_session: base.hSessions = self._get_session_by_name(session_name=session_name)
        if not h_session:
            return None
        if not self.__verify_password(plain_password=password, hashed_password=h_session.h_session_password):
            return None
        return SessionORMSchema.from_orm(h_session)
