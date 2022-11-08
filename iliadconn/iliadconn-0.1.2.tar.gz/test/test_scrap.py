import datetime
from unittest import TestCase
import requests_mock

from .data import html_iliad
from iliadconn import scrap


class TestScrap(TestCase):
    @requests_mock.Mocker()
    def test_normal(self, m):
        m.get('https://www.iliad.it/account/consumi-e-credito', status_code=200)
        m.post('https://www.iliad.it/account/consumi-e-credito', text=html_iliad)
        ret = scrap('user', 'password')
        self.assertEqual(ret, (datetime.datetime(2022, 11, 19, 0, 0), 67.18, 300, False))
