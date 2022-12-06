from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from typing import List, Optional

from src.funds.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.funds.orm import base
from src.funds.app import schemas


class WalletService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session

    def _get_all_wallets_by_label(self, label: str) -> List[Optional[schemas.wallets.WalletORMSchema]]:
        wallets = self._session.query(
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
        return [schemas.wallets.WalletORMSchema.from_orm(h_wallet) for h_wallet in wallets]

    def _get_wallet_by_fund(self, fund_id: int) -> Optional[schemas.wallets.WalletORMSchema]:
        wallet = self._session.query(
            base.HubAddresses.h_address,
            base.HubChains.h_network_name,
            base.HubChains.h_network_endpoint
        ).select_from(
            base.LinkAddressesLabelsChains
        ).join(
            base.LinkAddressesChains,
            base.LinkAddressesLabelsChains.l_address_chain_id == base.LinkAddressesChains.l_address_chain_id
        ).join(
            base.HubAddresses, base.LinkAddressesChains.h_address_id == base.HubAddresses.h_address_id
        ).join(
            base.HubChains, base.LinkAddressesChains.h_chain_id == base.HubChains.h_chain_id
        ).filter(
            base.LinkAddressesLabelsChains.l_address_label_chain_id == fund_id
        ).first()
        return schemas.wallets.WalletORMSchema.from_orm(wallet) if wallet else wallet

    def _get_address_by_address(self, address: str) -> Optional[base.HubAddresses]:
        return self._session.query(base.HubAddresses).filter_by(h_address=address).first()

    def _get_chain_by_name(self, name: str) -> Optional[base.HubChains]:
        return self._session.query(base.HubChains).filter_by(h_network_name=name).first()

    def _get_label_by_name(self, label: str) -> Optional[base.HubLabels]:
        return self._session.query(base.HubLabels).filter_by(h_label_name=label).first()

    def _get_wallet_by_chain_and_address(self, address_id: int, chain_id: int) -> Optional[base.LinkAddressesChains]:
        return self._session.query(base.LinkAddressesChains).filter_by(h_address_id=address_id, h_chain_id=chain_id).first()

    def _get_fund_by_wallet_id_and_label(self, label_id: int, wallet_id: int) -> base.LinkAddressesLabelsChains:
        return self._session.query(base.LinkAddressesLabelsChains).filter_by(l_address_chain_id=wallet_id, h_label_id=label_id).first()

    def _get_fund_by_address_and_chain_and_label(self, label_id: int, wallet_address: str, network_name: str) -> schemas.wallets.FundORMSchema:
        fund = self._session.query(
            base.LinkAddressesLabelsChains.l_address_label_chain_id,
            base.HubAddresses.h_address,
            base.HubChains.h_network_name,
            base.HubChains.h_network_endpoint
        ).select_from(
            base.LinkAddressesLabelsChains
        ).join(
            base.LinkAddressesChains,
            base.LinkAddressesLabelsChains.l_address_chain_id == base.LinkAddressesChains.l_address_chain_id
        ).join(
            base.HubAddresses,
            base.LinkAddressesChains.h_address_id == base.HubAddresses.h_address_id
        ).join(
            base.HubChains,
            base.LinkAddressesChains.h_chain_id == base.HubChains.h_chain_id
        ).join(
            base.HubLabels,
            base.LinkAddressesLabelsChains.h_label_id == base.HubLabels.h_label_id
        ).filter(
            base.HubLabels.h_label_id == label_id,
            base.HubAddresses.h_address == wallet_address,
            base.HubChains.h_network_name == network_name
        ).first()

        return schemas.wallets.FundORMSchema.from_orm(fund) if fund else fund

    def on_get__wallets_all(self, label: str) -> List[Optional[schemas.wallets.WalletORMSchema]]:
        return self._get_all_wallets_by_label(label=label)

    def on_post__wallets_add(self, address: str, chain: str, label: str) -> Optional[schemas.wallets.WalletORMSchema]:
        h_label: base.HubLabels = self._get_label_by_name(label=label)
        if not h_label:
            return None
        h_chain: base.HubChains = self._get_chain_by_name(name=chain)
        if not h_chain:
            return None

        h_address: base.HubAddresses = self._get_address_by_address(address=address)
        if not h_address:
            h_address: base.HubAddresses = base.HubAddresses(
                h_address=address
            )
            self._session.add(h_address)
            self._session.commit()
        l_address_chain: base.LinkAddressesChains = self._get_wallet_by_chain_and_address(
            address_id=h_address.h_address_id,
            chain_id=h_chain.h_chain_id
        )
        if not l_address_chain:
            l_address_chain: base.LinkAddressesChains = base.LinkAddressesChains(
                h_address_id=h_address.h_address_id,
                h_chain_id=h_chain.h_chain_id
            )
            self._session.add(l_address_chain)
            self._session.commit()
        l_address_label_chain: base.LinkAddressesLabelsChains = self._get_fund_by_wallet_id_and_label(
            label_id=h_label.h_label_id,
            wallet_id=l_address_chain.l_address_chain_id
        )
        if not l_address_label_chain:
            l_address_label_chain: base.LinkAddressesLabelsChains = base.LinkAddressesLabelsChains(
                l_address_chain_id=l_address_chain.l_address_chain_id,
                h_label_id=h_label.h_label_id
            )
            self._session.add(l_address_label_chain)
            self._session.commit()
            return self._get_wallet_by_fund(fund_id=l_address_label_chain.l_address_label_chain_id)
        return None

    def on_get__wallets_get_fund(self, wallet_address: str, network_name: str, label_id: int) -> Optional[schemas.wallets.FundORMSchema]:
        return self._get_fund_by_address_and_chain_and_label(
            wallet_address=wallet_address,
            network_name=network_name,
            label_id=label_id
        )

    def on_delete__wallets_delete_fund(self, wallet_address: str, network_name: str, label_id: int) -> bool:
        fund: schemas.wallets.FundORMSchema = self._get_fund_by_address_and_chain_and_label(
            wallet_address=wallet_address,
            network_name=network_name,
            label_id=label_id
        )
        if fund:
            self._session.query(base.LinkAddressesLabelsChains).filter_by(l_address_label_chain_id=fund.l_address_label_chain_id).delete()
            self._session.commit()
            return True
        return False

