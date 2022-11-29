from sqlalchemy.orm import Session

import random
import string
import hashlib

from funds.app.forms.labels.forms import LabelForm
from funds.orm.base import HubLabels


class PasswordBase:

    @staticmethod
    def _get_salt(length=16) -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def _hash_password(self, password: str, salt: str = None) -> str:
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode() if salt else self._get_salt(),
            100_000
        ).hex()


class LabelBase(PasswordBase):
    _session: Session = None

    def _create_label(self, label: LabelForm) -> str:
        salt: str = self._get_salt()
        hashed_password: str = self._hash_password(password=label.password, salt=salt)
        model: HubLabels = HubLabels(
            h_label_name=label.name,
            h_label_password=f'{salt}${hashed_password}'
        )
        self._session.add(model)
        self._session.commit()
        return f"Label {model.h_label_name} successfully created"

    def _get_label_by_name(self, label: str) -> HubLabels:
        return self._session.query(HubLabels).filter_by(h_label_name=label).first()
