import os
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.orm.base import hSessions
from app.orm.cfg.engine import ORMSettings


ADMIN_SESSION = os.getenv('ADMIN_SESSION', '')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '')


if __name__ == '__main__':
    c = CryptContext(schemes=['bcrypt'], deprecated='auto')
    s = Session(ORMSettings.get_engine())

    h_session = s.query(hSessions).filter_by(h_session_name=ADMIN_SESSION).first()
    if not h_session:
        h_session = hSessions(
            h_session_name=ADMIN_SESSION,
            h_session_password=c.hash(secret=ADMIN_PASSWORD)
        )
        s.add(h_session)
        s.commit()
