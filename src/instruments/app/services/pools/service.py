from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from typing import List, Optional

from src.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.orm import base
from src.instruments.app import schemas
from src.funds.app import schemas as funds_schemas


class PoolService:

    def __init__(self, session: Session = Depends(ORMSettings.get_session)):
        self._session: Session = session

    def _get_fund_by_address_and_chain_and_label(
            self,
            label_id: int,
            wallet_address: str,
            network_name: str
    ) -> funds_schemas.wallets.FundORMSchema:
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

        return funds_schemas.wallets.FundORMSchema.from_orm(fund) if fund else fund

    def _get_pool_by_id(self, pool_id: int) -> Optional[schemas.pools.PoolORMSchema]:
        pool = self._session.query(
            base.LinkAddressesChains.l_address_chain_name,
            base.HubAddresses.h_address,
            base.HubChains.h_network_name,
            base.HubChains.h_network_endpoint,
            base.HubProtocols.h_protocol_name,
            base.HubProtocolsCategories.h_protocol_category_name
        ).select_from(
            base.LinkAddressesProtocolsCategoriesChains
        ).join(
            base.LinkProtocolsCategoriesChains, base.LinkAddressesProtocolsCategoriesChains.l_protocol_category_chain_id == base.LinkProtocolsCategoriesChains.l_protocol_category_chain_id
        ).join(
            base.LinkProtocolsCategories, base.LinkProtocolsCategoriesChains.l_protocol_category_id == base.LinkProtocolsCategories.l_protocol_category_id
        ).join(
            base.HubProtocols, base.LinkProtocolsCategories.h_protocol_id == base.HubProtocols.h_protocol_id
        ).join(
            base.HubProtocolsCategories, base.LinkProtocolsCategories.h_protocol_category_id == base.HubProtocolsCategories.h_protocol_category_id
        ).join(
            base.LinkAddressesChains, base.LinkAddressesProtocolsCategoriesChains.l_address_chain_id == base.LinkAddressesChains.l_address_chain_id
        ).join(
            base.HubAddresses, base.LinkAddressesChains.h_address_id == base.HubAddresses.h_address_id
        ).join(
            base.HubChains, base.LinkAddressesChains.h_chain_id == base.HubChains.h_chain_id
        ).filter(
            base.LinkAddressesProtocolsCategoriesChains.l_address_protocol_category_chain_id == pool_id
        ).first()
        return schemas.pools.PoolORMSchema.from_orm(pool) if pool else pool

    def _get_pool_by_params(
            self,
            pool_address: str,
            chain: str,
            protocol: str,
            protocol_category: str,
            fund_id: int
    ) -> Optional[base.LinkAddressesProtocolsCategoriesChains]:

        pool = self._session.query(
            base.LinkAddressesProtocolsCategoriesChains
        ).select_from(
            base.LinkAddressesProtocolsCategoriesChains
        ).join(
            base.LinkProtocolsCategoriesChains,
            base.LinkAddressesProtocolsCategoriesChains.l_protocol_category_chain_id == base.LinkProtocolsCategoriesChains.l_protocol_category_chain_id
        ).join(
            base.LinkProtocolsCategories,
            base.LinkProtocolsCategoriesChains.l_protocol_category_id == base.LinkProtocolsCategories.l_protocol_category_id
        ).join(
            base.HubProtocols,
            base.LinkProtocolsCategories.h_protocol_id == base.HubProtocols.h_protocol_id
        ).join(
            base.HubProtocolsCategories,
            base.LinkProtocolsCategories.h_protocol_category_id == base.HubProtocolsCategories.h_protocol_category_id
        ).join(
            base.LinkAddressesChains,
            base.LinkAddressesProtocolsCategoriesChains.l_address_chain_id == base.LinkAddressesChains.l_address_chain_id
        ).join(
            base.HubAddresses,
            base.LinkAddressesChains.h_address_id == base.HubAddresses.h_address_id
        ).join(
            base.HubChains,
            base.LinkAddressesChains.h_chain_id == base.HubChains.h_chain_id
        ).join(
            base.LinkAddressesLabelsChains,
            base.LinkAddressesProtocolsCategoriesChains.l_address_label_chain_id == base.LinkAddressesLabelsChains.l_address_label_chain_id
        ).join(
            base.HubLabels,
            base.LinkAddressesLabelsChains.h_label_id == base.HubLabels.h_label_id
        ).filter(
            base.HubAddresses.h_address == pool_address,
            base.LinkAddressesLabelsChains.l_address_label_chain_id == fund_id,
            base.HubChains.h_network_name == chain,
            base.HubProtocols.h_protocol_name == protocol,
            base.HubProtocolsCategories.h_protocol_category_name == protocol_category
        ).first()
        return pool

    def _get_address_by_address(self, address: str) -> Optional[base.HubAddresses]:
        return self._session.query(base.HubAddresses).filter_by(h_address=address).first()

    def _get_chain_by_name(self, name: str) -> Optional[base.HubChains]:
        return self._session.query(base.HubChains).filter_by(h_network_name=name).first()

    def _get_label_by_name(self, label: str) -> Optional[base.HubLabels]:
        return self._session.query(base.HubLabels).filter_by(h_label_name=label).first()

    def _get_protocol_by_name(self, protocol: str) -> Optional[base.HubProtocols]:
        return self._session.query(base.HubProtocols).filter_by(h_protocol_name=protocol).first()

    def _get_protocol_category_by_name(self, protocol_category: str) -> Optional[base.HubProtocolsCategories]:
        return self._session.query(base.HubProtocolsCategories).filter_by(h_protocol_category_name=protocol_category).first()

    def _get_address_on_chain_by_chain_and_address(self, address_id: int, chain_id: int) -> Optional[base.LinkAddressesChains]:
        return self._session.query(base.LinkAddressesChains).filter_by(h_address_id=address_id, h_chain_id=chain_id).first()

    def _get_protocol_type_by_protocol_and_category(self, protocol_id: int, category_id: int) -> Optional[base.LinkProtocolsCategories]:
        return self._session.query(base.LinkProtocolsCategories).filter_by(h_protocol_id=protocol_id, h_protocol_category_id=category_id).first()

    def _get_protocol_type_on_chain_by_protocol_type_and_chain(self, protocol_type_id: int, chain_id: int) -> Optional[base.LinkProtocolsCategoriesChains]:
        return self._session.query(base.LinkProtocolsCategoriesChains).filter_by(l_protocol_category_id=protocol_type_id, h_chain_id=chain_id).first()

    def _get_fund_by_wallet_id_and_label(self, label_id: int, wallet_id: int) -> base.LinkAddressesLabelsChains:
        return self._session.query(base.LinkAddressesLabelsChains).filter_by(l_address_chain_id=wallet_id, h_label_id=label_id).first()

    def _get_pool_by_protocol_type_on_chain_and_fund_and_address(self, fund_id: int, protocol_type_id: int, address_id: int) -> Optional[base.LinkAddressesProtocolsCategoriesChains]:
        return self._session.query(base.LinkAddressesProtocolsCategoriesChains).filter_by(l_protocol_category_chain_id=protocol_type_id, l_address_chain_id=address_id, l_address_label_chain_id=fund_id).first()

    def on_post__pools_add_pool(
            self,
            pool_address: str,
            pool_name: str,
            wallet_address: str,
            chain: str,
            label: str,
            protocol: str,
            protocol_category: str
    ) -> Optional[schemas.pools.PoolORMSchema]:
        h_label: base.HubLabels = self._get_label_by_name(label=label)
        if not h_label:
            return None
        h_chain: base.HubChains = self._get_chain_by_name(name=chain)
        if not h_chain:
            return None
        h_wallet_address: base.HubAddresses = self._get_address_by_address(address=wallet_address)
        if not h_wallet_address:
            return None
        h_protocol: base.HubProtocols = self._get_protocol_by_name(protocol=protocol)
        if not h_protocol:
            return None
        h_protocol_category: base.HubProtocolsCategories = self._get_protocol_category_by_name(protocol_category=protocol_category)
        if not h_protocol_category:
            return None
        l_protocol_category: base.LinkProtocolsCategories = self._get_protocol_type_by_protocol_and_category(
            protocol_id=h_protocol.h_protocol_id,
            category_id=h_protocol_category.h_protocol_category_id
        )
        if not l_protocol_category:
            return None
        l_protocol_category_chain: base.LinkProtocolsCategoriesChains = self._get_protocol_type_on_chain_by_protocol_type_and_chain(
            protocol_type_id=l_protocol_category.l_protocol_category_id,
            chain_id=h_chain.h_chain_id
        )
        if not l_protocol_category_chain:
            return None
        l_wallet_address_chain: base.LinkAddressesChains = self._get_address_on_chain_by_chain_and_address(
            address_id=h_wallet_address.h_address_id,
            chain_id=h_chain.h_chain_id
        )
        if not l_wallet_address_chain:
            return None
        l_address_label_chain: base.LinkAddressesLabelsChains = self._get_fund_by_wallet_id_and_label(
            label_id=h_label.h_label_id,
            wallet_id=l_wallet_address_chain.l_address_chain_id
        )
        if not l_address_label_chain:
            return None

        h_pool_address: base.HubAddresses = self._get_address_by_address(address=pool_address)
        if not h_pool_address:
            h_pool_address: base.HubAddresses = base.HubAddresses(
                h_address=pool_address
            )
            self._session.add(h_pool_address)
            self._session.commit()
        l_pool_address_chain: base.LinkAddressesChains = self._get_address_on_chain_by_chain_and_address(
            address_id=h_pool_address.h_address_id,
            chain_id=h_chain.h_chain_id
        )
        if not l_pool_address_chain:
            l_pool_address_chain: base.LinkAddressesChains = base.LinkAddressesChains(
                h_address_id=h_pool_address.h_address_id,
                h_chain_id=h_chain.h_chain_id,
                l_address_chain_name=pool_name

            )
            self._session.add(l_pool_address_chain)
            self._session.commit()

        pool: base.LinkAddressesProtocolsCategoriesChains = self._get_pool_by_protocol_type_on_chain_and_fund_and_address(
            fund_id=l_address_label_chain.l_address_label_chain_id,
            protocol_type_id=l_protocol_category_chain.l_protocol_category_chain_id,
            address_id=l_pool_address_chain.l_address_chain_id
        )
        if not pool:
            pool: base.LinkAddressesProtocolsCategoriesChains = base.LinkAddressesProtocolsCategoriesChains(
                l_protocol_category_chain_id=l_protocol_category_chain.l_protocol_category_chain_id,
                l_address_chain_id=l_pool_address_chain.l_address_chain_id,
                l_address_label_chain_id=l_address_label_chain.l_address_label_chain_id
            )
            self._session.add(pool)
            self._session.commit()
            return self._get_pool_by_id(pool_id=pool.l_address_protocol_category_chain_id)
        return None

    def on_delete__pools_delete_pool(
            self,
            pool_address: str,
            wallet_address: str,
            chain: str,
            label_id: int,
            protocol: str,
            protocol_category: str
    ) -> bool:
        fund_id: int = self._get_fund_by_address_and_chain_and_label(
            label_id=label_id,
            wallet_address=wallet_address,
            network_name=chain
        ).l_address_label_chain_id
        if not fund_id:
            return False

        pool: base.LinkAddressesProtocolsCategoriesChains = self._get_pool_by_params(
            pool_address=pool_address,
            chain=chain,
            protocol=protocol,
            protocol_category=protocol_category,
            fund_id=fund_id
        )
        if pool:
            self._session.query(base.LinkAddressesProtocolsCategoriesChains).filter_by(l_address_protocol_category_chain_id=pool.l_address_protocol_category_chain_id).delete()
            self._session.commit()
            return True
        return False

