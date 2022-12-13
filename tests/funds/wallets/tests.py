import json
import random

from fastapi import status
from eth_account import Account
import secrets
from web3 import Web3

from src.cfg.settings import settings


class TestWalletCBV:

    @classmethod
    def setup_class(cls):
        cls.addresses = [
            cls.address_generator() for _ in range(random.randint(8, 32))
        ]

    @classmethod
    def teardown_class(cls):
        ...

    @staticmethod
    def address_generator():
        return Account.from_key(f'0x{secrets.token_hex(32)}').address

    def test_on_post__wallets_add(self, client, jwt_token, h_chains):

        for address in self.addresses:
            for h_chain in h_chains:
                json_ = json.dumps(
                    {
                        'address': address,
                        'chain': h_chain.h_network_name
                    }
                )
                response = client.post(f'{settings.API_V1}/funds/wallets/add', content=json_, headers=jwt_token)

                assert response.status_code == status.HTTP_201_CREATED
                assert isinstance(response.json()['h_address'], str)
                assert Web3.isAddress(response.json()['h_address'])
                assert isinstance(response.json()['h_network_name'], str)
                assert isinstance(response.json()['h_network_endpoint'], str)

    def test_on_get__wallets_all(self, client, jwt_token):
        response = client.get(f'{settings.API_V1}/funds/wallets/all', headers=jwt_token)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        for wallet in response.json():
            assert isinstance(wallet['h_address'], str)
            assert Web3.isAddress(wallet['h_address'])
            assert isinstance(wallet['h_network_name'], str)
            assert isinstance(wallet['h_network_endpoint'], str)

    def test_on_get__wallets_get_fund(self, client, jwt_token, h_chains):
        for address in self.addresses:
            for h_chain in h_chains:
                response = client.get(f'{settings.API_V1}/funds/wallets/{h_chain.h_network_name}/{address}', headers=jwt_token)

                assert response.status_code == status.HTTP_200_OK
                assert isinstance(response.json()['h_address'], str)
                assert Web3.isAddress(response.json()['h_address'])
                assert isinstance(response.json()['h_network_name'], str)
                assert isinstance(response.json()['h_network_endpoint'], str)

    def test_on_delete__wallets_delete_fund(self, client, jwt_token, h_chains):
        for address in self.addresses:
            for h_chain in h_chains:
                response = client.delete(f'{settings.API_V1}/funds/wallets/{h_chain.h_network_name}/{address}', headers=jwt_token)

                assert response.status_code == status.HTTP_202_ACCEPTED
                assert isinstance(response.json()['address'], str)
                assert Web3.isAddress(response.json()['address'])
                assert isinstance(response.json()['chain'], str)

                response = client.get(f'{settings.API_V1}/funds/wallets/{h_chain.h_network_name}/{address}', headers=jwt_token)
                assert response.status_code == status.HTTP_404_NOT_FOUND
