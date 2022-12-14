import json
import random

import pytest
from fastapi import status
from web3 import Web3

from src.cfg.settings import settings

from tests.funds.wallets.tests import TestWalletCBV
from tests.funds.labels.tests import TestLabelCBV


class TestAllocationCBV:

    @classmethod
    def setup_class(cls):
        cls.walletAddresses = [
            TestWalletCBV.address_generator() for _ in range(random.randint(8, 16))
        ]
        cls.poolAddresses = [
            TestWalletCBV.address_generator() for _ in range(random.randint(8, 16))
        ]

    @classmethod
    def teardown_class(cls):
        ...

    @pytest.fixture()
    def wallets(self, client, h_chains, jwt_token):
        wallets = [
            client.post(
                f'{settings.API_V1}/funds/wallets/add',
                content=json.dumps(
                    {
                        'address': address,
                        'chain': h_chain.h_network_name
                    }
                ),
                headers=jwt_token
            ).json()
            for address in self.walletAddresses
            for h_chain in h_chains
        ]
        return wallets

    @pytest.fixture()
    def allocations(
            self,
            h_protocols, h_protocols_categories,
            l_protocols_categories, l_protocols_categories_chains
    ):
        pool_name = TestLabelCBV.str_generator(size=random.randint(6, 18))
        pools = list(
            map(lambda address: list(
                map(lambda h_protocol: list(
                    map(lambda h_protocol_category: json.dumps(
                {
                    'address': address,
                    'protocol': h_protocol.h_protocol_name,
                    'protocol_category': h_protocol_category.h_protocol_category_name,
                    'pool_name': pool_name
                }
            ),
                        h_protocols_categories)),
                    h_protocols)),
                self.poolAddresses))
        return [pool for _ in pools for __ in _ for pool in __]

    def test_on_post__allocations_add_allocation(
            self,
            client, jwt_token,
            h_protocols, h_protocols_categories,
            l_protocols_categories, l_protocols_categories_chains,
            wallets, allocations
    ):
        for wallet in wallets:
            for pool in allocations:
                response = client.post(f"{settings.API_V1}/instruments/allocations/{wallet['h_network_name']}/{wallet['h_address']}", content=pool, headers=jwt_token)

                assert response.status_code == status.HTTP_201_CREATED

                assert isinstance(response.json()['l_address_chain_name'], str)
                assert response.json()['l_address_chain_name'] == json.loads(pool)['pool_name']

                assert isinstance(response.json()['h_address'], str)
                assert Web3.isAddress(response.json()['h_address'])
                assert response.json()['h_address'] == json.loads(pool)['address']

                assert isinstance(response.json()['h_network_name'], str)
                assert isinstance(response.json()['h_network_endpoint'], str)

                assert isinstance(response.json()['h_protocol_name'], str)
                assert response.json()['h_protocol_name'] == json.loads(pool)['protocol']

                assert isinstance(response.json()['h_protocol_category_name'], str)
                assert response.json()['h_protocol_category_name'] == json.loads(pool)['protocol_category']

    def test_on_delete__allocations_delete_allocation(
            self,
            client, jwt_token,
            h_protocols, h_protocols_categories,
            l_protocols_categories, l_protocols_categories_chains,
            allocations
    ):
        response = client.get(f"{settings.API_V1}/funds/wallets/all", headers=jwt_token)
        for wallet in response.json():
            for pool in allocations:
                pool_ = json.loads(pool)
                response = client.delete(
                    f"{settings.API_V1}/instruments/allocations/"
                    f"{wallet['h_network_name']}/"
                    f"{wallet['h_address']}/"
                    f"{pool_['protocol']}/"
                    f"{pool_['protocol_category']}/"
                    f"{pool_['address']}/"
                    f"{pool_['pool_name']}",
                    headers=jwt_token
                )

                assert response.status_code == status.HTTP_202_ACCEPTED
                assert isinstance(response.json()['address'], str)
                assert Web3.isAddress(response.json()['address'])
                assert isinstance(response.json()['protocol'], str)
                assert isinstance(response.json()['protocol_category'], str)
                assert isinstance(response.json()['pool_name'], str)
