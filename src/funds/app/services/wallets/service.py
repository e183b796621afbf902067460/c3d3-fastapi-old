from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from typing import List

from src.funds.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.funds.orm import base
from src.funds.app import schemas


class WalletService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session

    def _get_all_wallets_by_label(self, label: str) -> List[schemas.wallets.WalletORMSchema]:
        h_wallets = self._session.query(
                base.HubAddresses.h_address,
                base.HubChains.h_network_name,
                base.HubChains.h_network_endpoint
            ).select_from(
                base.HubLabels
            ).join(
                base.LinkAddressesLabelsChains, base.HubLabels.h_label_id == base.LinkAddressesLabelsChains.h_label_id
            ).join(
                base.LinkAddressesChains, base.LinkAddressesLabelsChains.l_address_chain_id == base.LinkAddressesChains.l_address_chain_id
            ).join(
                base.HubAddresses, base.LinkAddressesChains.h_address_id == base.HubAddresses.h_address_id
            ).join(
                base.HubChains, base.LinkAddressesChains.h_chain_id == base.HubChains.h_chain_id
            ).filter(
                base.HubLabels.h_label_name == label
            ).all()
        return [schemas.wallets.WalletORMSchema.from_orm(h_wallet) for h_wallet in h_wallets]

    def on_get__wallets_all(self, label: str) -> List[schemas.wallets.WalletORMSchema]:
        return self._get_all_wallets_by_label(label=label)

