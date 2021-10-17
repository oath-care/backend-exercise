from json import JSONDecodeError

from django.test import TestCase

from rest_framework import status
from rest_framework.test import RequestsClient

HOST = 'http://127.0.0.1:8000/app'

user_1_params = {
    "first_name": "Danny",
    "last_name": "Rup",
    "date_of_birth": "1965-08-12",
    "city": "Berlin",
    "state": None,
    "country": "Germany",
}

user_2_params = {
    "id": 2,
    "first_name": "James",
    "last_name": "Cantore",
    "date_of_birth": "1964-02-16",
    "city": "Beacon Falls",
    "state": "Connecticut",
    "country": "United States",
}


class CreateUserTest(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + '/users/'

    def test_user_creation(self):
        r = self.client.post(self.url, data=user_1_params)
        self.assertEquals(r.status_code, status.HTTP_201_CREATED)
        data = r.json()
        self.assertIn('id', data)
        self.assertTrue(isinstance(data['id'], int))
        del data['id']
        self.assertDictEqual(user_1_params, data)


class TestGetAllUsers(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + '/users/'

        users = [
            user_1_params,
            user_2_params
        ]

        try:
            self.users = [self.client.post(self.url, data=user).json() for user in users]
        except JSONDecodeError as ex:
            self.fail(f'/users/ endpoint for POST request not implemented correctly. Error [{ex}]')
        self.users.sort(key=lambda user: user['id'])

    def test_get_all_users(self):
        r = self.client.get(self.url)
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(self.users, data)


class TestGetUser(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + '/users/{}/'
        try:
            self.users = [self.client.post(HOST + '/users/', data=user).json() for user in
                          [user_1_params, user_2_params]]
        except JSONDecodeError:
            self.fail('/users/ users endpoint for POST request not implemented correctly')

    def test_get_retrieve_existing_id(self):
        for user in self.users:
            user_id = user['id']
            try:
                r = self.client.get(self.url.format(user_id))
            except JSONDecodeError:
                self.fail('/users/:user_id endpoint for GET request not implemented correctly')
            self.assertEquals(r.status_code, status.HTTP_200_OK)
            data = r.json()
            self.assertDictEqual(user, data)

    def test_get_retrieve_non_existing_id(self):
        try:
            r = self.client.get(self.url.format(10000))
        except JSONDecodeError:
            self.fail('/users/:user_id endpoint for GET request not implemented correctly')
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)
