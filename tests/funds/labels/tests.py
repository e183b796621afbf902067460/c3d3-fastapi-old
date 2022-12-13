import json
import random
import string

from fastapi import status

from src.cfg.settings import settings


class TestLabelCBV:

    @classmethod
    def setup_class(cls):
        cls.oauth2_ = [
            {
                'username': cls.str_generator(size=random.randint(6, 18)),
                'password': cls.str_generator(size=random.randint(6, 18))
            }
            for _ in range(random.randint(8, 32))
        ]

    @classmethod
    def teardown_class(cls):
        ...

    @staticmethod
    def str_generator(size: int, chars: str = string.ascii_letters):
        return ''.join(random.choice(chars) for _ in range(size))

    def test_on_post__label_sign_up(self, client):

        for i, oauth2_ in enumerate(self.oauth2_):
            json_ = json.dumps(oauth2_)

            response = client.post(f'{settings.API_V1}/funds/labels/sign-up', content=json_)
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json()['h_label_name'] == oauth2_['username']

    def test_on_post__label_sign_in(self, client):

        for i, oauth2_ in enumerate(self.oauth2_):
            header = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = client.post(f'{settings.API_V1}/funds/labels/sign-in', data=oauth2_, headers=header)
            assert response.status_code == status.HTTP_200_OK
            assert isinstance(response.json()['access_token'], str)
            assert isinstance(response.json()['refresh_token'], str)

    def test_on_post__label_account(self, client, jwt_token):
        response = client.get(f'{settings.API_V1}/funds/labels/account', headers=jwt_token)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json()['h_label_id'], int)
        assert isinstance(response.json()['h_label_name'], str)