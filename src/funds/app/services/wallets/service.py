from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from src.funds.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.funds.orm import base
from src.funds.app import schemas


class WalletService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session
