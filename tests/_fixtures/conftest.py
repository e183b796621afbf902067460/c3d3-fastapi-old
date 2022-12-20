import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

from src.orm.base.main import Base
from src.orm import base

from tests._fixtures.cfg import FIXTURE
from tests.conftest import TestORMSettings


URI = TestORMSettings.get_uri()
ENGINE = TestORMSettings.get_engine()


@pytest.fixture(scope='session')
def environment() -> None:
    if database_exists(URI):
        drop_database(URI)
    create_database(URI)
    Base.metadata.create_all(ENGINE)


@pytest.fixture(scope="session")
def session(environment):
    s = sessionmaker(ENGINE)
    yield s()
    s.close_all()


@pytest.fixture(scope='session')
def _fixtures(session):
    for l_address_chain_name, conf in FIXTURE.items():

        # TODO Hubs
        h_protocol = session.query(base.HubProtocols).filter_by(
            h_protocol_name=conf['h_protocols']['h_protocol_name']
        ).first()
        if not h_protocol:
            h_protocol = base.HubProtocols(
                h_protocol_name=conf['h_protocols']['h_protocol_name']
            )

        h_protocol_category = session.query(base.HubProtocolsCategories).filter_by(
            h_protocol_category_name=conf['h_protocols_categories']['h_protocol_category_name']
        ).first()
        if not h_protocol_category:
            h_protocol_category = base.HubProtocolsCategories(
                h_protocol_category_name=conf['h_protocols_categories']['h_protocol_category_name']
            )

        h_chain = session.query(base.HubChains).filter_by(
            h_network_name=conf['h_chains']['h_network_name'],
            h_network_id=conf['h_chains']['h_network_id']
        ).first()
        if not h_chain:
            h_chain = base.HubChains(
                h_network_name=conf['h_chains']['h_network_name'],
                h_network_id=conf['h_chains']['h_network_id'],
                h_network_endpoint=conf['h_chains']['h_network_endpoint']
            )

        h_address_pool = session.query(base.HubAddresses).filter_by(
            h_address=conf['h_addresses']['h_pool_address']
        ).first()
        if not h_address_pool:
            h_address_pool = base.HubAddresses(
                h_address=conf['h_addresses']['h_pool_address']
            )

        h_address_wallet = session.query(base.HubAddresses).filter_by(
            h_address=conf['h_addresses']['h_wallet_address']
        ).first()
        if not h_address_wallet:
            h_address_wallet = base.HubAddresses(
                h_address=conf['h_addresses']['h_wallet_address']
            )

        h_label = session.query(base.HubLabels).filter_by(
            h_label_name=conf['h_labels']['h_label_name']
        ).first()
        if not h_label:
            h_label = base.HubLabels(
                h_label_name=conf['h_labels']['h_label_name'],
                h_label_password=conf['h_labels']['h_label_password']
            )

        hubs = [
            h_protocol,
            h_protocol_category,
            h_chain,
            h_address_pool,
            h_address_wallet,
            h_label
        ]
        session.add_all(hubs)
        session.commit()

        # TODO FirstLinks
        l_protocol_category = session.query(base.LinkProtocolsCategories).filter_by(
            h_protocol_id=h_protocol.h_protocol_id,
            h_protocol_category_id=h_protocol_category.h_protocol_category_id
        ).first()
        if not l_protocol_category:
            l_protocol_category = base.LinkProtocolsCategories(
                h_protocol_id=h_protocol.h_protocol_id,
                h_protocol_category_id=h_protocol_category.h_protocol_category_id
            )

        l_address_chain_pool = session.query(base.LinkAddressesChains).filter_by(
            h_address_id=h_address_pool.h_address_id,
            h_chain_id=h_chain.h_chain_id,
            l_address_chain_name=l_address_chain_name
        ).first()
        if not l_address_chain_pool:
            l_address_chain_pool = base.LinkAddressesChains(
                h_address_id=h_address_pool.h_address_id,
                h_chain_id=h_chain.h_chain_id,
                l_address_chain_name=l_address_chain_name
            )

        l_address_chain_wallet = session.query(base.LinkAddressesChains).filter_by(
            h_address_id=h_address_wallet.h_address_id,
            h_chain_id=h_chain.h_chain_id
        ).first()
        if not l_address_chain_wallet:
            l_address_chain_wallet = base.LinkAddressesChains(
                h_address_id=h_address_wallet.h_address_id,
                h_chain_id=h_chain.h_chain_id
            )

        links = [
            l_protocol_category,
            l_address_chain_pool,
            l_address_chain_wallet
        ]
        session.add_all(links)
        session.commit()

        # TODO SecondLinks
        l_protocol_category_chain = session.query(base.LinkProtocolsCategoriesChains).filter_by(
            l_protocol_category_id=l_protocol_category.l_protocol_category_id,
            h_chain_id=h_chain.h_chain_id
        ).first()
        if not l_protocol_category_chain:
            l_protocol_category_chain = base.LinkProtocolsCategoriesChains(
                l_protocol_category_id=l_protocol_category.l_protocol_category_id,
                h_chain_id=h_chain.h_chain_id
            )

        l_address_label_chain = session.query(base.LinkAddressesLabelsChains).filter_by(
            l_address_chain_id=l_address_chain_wallet.l_address_chain_id,
            h_label_id=h_label.h_label_id
        ).first()
        if not l_address_label_chain:
            l_address_label_chain = base.LinkAddressesLabelsChains(
                l_address_chain_id=l_address_chain_wallet.l_address_chain_id,
                h_label_id=h_label.h_label_id
            )
        links = [
            l_address_label_chain,
            l_protocol_category_chain
        ]
        session.add_all(links)
        session.commit()

        # TODO Pool
        l_address_protocol_category_chain = session.query(base.LinkAddressesProtocolsCategoriesChains).filter_by(
            l_protocol_category_chain_id=l_protocol_category_chain.l_protocol_category_chain_id,
            l_address_chain_id=l_address_chain_pool.l_address_chain_id,
            l_address_label_chain_id=l_address_label_chain.l_address_label_chain_id
        ).first()
        if not l_address_protocol_category_chain:
            l_address_protocol_category_chain = base.LinkAddressesProtocolsCategoriesChains(
                l_protocol_category_chain_id=l_protocol_category_chain.l_protocol_category_chain_id,
                l_address_chain_id=l_address_chain_pool.l_address_chain_id,
                l_address_label_chain_id=l_address_label_chain.l_address_label_chain_id
            )
        session.add(l_address_protocol_category_chain)
        session.commit()

        # TODO Allocation
        s_address_protocol_category_label_chain = session.query(base.SatelliteAddressesProtocolsCategoriesLabelsChains).filter_by(
            l_address_protocol_category_chain_id=l_address_protocol_category_chain.l_address_protocol_category_chain_id
        ).first()
        if not s_address_protocol_category_label_chain:
            s_address_protocol_category_label_chain = base.SatelliteAddressesProtocolsCategoriesLabelsChains(
                l_address_protocol_category_chain_id=l_address_protocol_category_chain.l_address_protocol_category_chain_id
            )
        session.add(s_address_protocol_category_label_chain)
        session.commit()


def test(_fixtures):
    pass