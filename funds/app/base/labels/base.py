from sqlalchemy.orm import Session

import random
import string
import hashlib

from funds.app.forms.labels.forms import LabelForm
from funds.orm.base import HubLabels


class PasswordBase:  # Add IBase to defi-head-core
    _session: Session = None

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

    def _validate_password(self, password: str, hashed_password: str) -> bool:
        salt, hash_ = hashed_password.split('$')
        return self._hash_password(password=password, salt=salt) == hash_


class LabelBase(PasswordBase):

    def _create_label(self, label: LabelForm) -> HubLabels:
        salt: str = self._get_salt()
        hashed_password: str = self._hash_password(password=label.password, salt=salt)
        model: HubLabels = HubLabels(
            h_label_name=label.name,
            h_label_password=f'{salt}${hashed_password}'
        )
        self._session.add(model)
        self._session.commit()
        return model

    def _get_label_by_name(self, label: str) -> HubLabels:
        return self._session.query(
            HubLabels
        ).filter_by(
            h_label_name=label
        ).first()

    def _get_label_by_id(self, id_: str) -> HubLabels:
        return self._session.query(
            HubLabels
        ).filter_by(
            h_label_id=id_
        ).first()
