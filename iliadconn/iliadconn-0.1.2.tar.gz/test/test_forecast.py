import datetime
from unittest import TestCase

from iliadconn import calc_forecast, calc_current_subscription
from freezegun import freeze_time


class TestForecast(TestCase):

    @freeze_time("2022-10-28")
    def test_normal(self):
        date_next_subscription = datetime.datetime.fromisoformat('2022-11-19T00:00')
        ret = calc_forecast(date_next_subscription, 39.44, 300, False)
        self.assertEqual(ret, 'iliad: 39.44/300GB (136GB/m ✓)')

    @freeze_time("2022-10-19")
    def test_now_on_start(self):
        date_next_subscription = datetime.datetime.fromisoformat('2022-11-19T00:00')
        ret = calc_forecast(date_next_subscription, 0.5, 300, False)
        self.assertEqual(ret, 'iliad: 0.5/300GB (16GB/m ✓)')

    @freeze_time("2022-11-18")
    def test_now_on_end(self):
        date_next_subscription = datetime.datetime.fromisoformat('2022-11-19T00:00')
        ret = calc_forecast(date_next_subscription, 170, 300, False)
        self.assertEqual(ret, 'iliad: 170/300GB (176GB/m ✓)')

    @freeze_time("2022-11-18")
    def test_calc_current_subscription_on_end(self):
        date_next_subscription = datetime.datetime.fromisoformat('2022-11-19T00:00')
        ret = calc_current_subscription(date_next_subscription)
        self.assertEqual(ret, (datetime.datetime(2022, 10, 19, 0, 0), datetime.datetime(2022, 11, 19, 0, 0)))

    @freeze_time("2022-10-19")
    def test_calc_current_subscription_on_start(self):
        date_next_subscription = datetime.datetime.fromisoformat('2022-11-19T00:00')
        ret = calc_current_subscription(date_next_subscription)
        self.assertEqual(ret, (datetime.datetime(2022, 10, 19, 0, 0), datetime.datetime(2022, 11, 19, 0, 0)))

    @freeze_time("2022-09-20")
    def test_calc_current_subscription_two_months_ago(self):
        date_next_subscription = datetime.datetime.fromisoformat('2022-11-19T00:00')
        ret = calc_current_subscription(date_next_subscription)
        self.assertEqual(ret, (datetime.datetime(2022, 9, 19, 0, 0), datetime.datetime(2022, 10, 19, 0, 0)))

    @freeze_time("2022-07-20")
    def test_calc_current_subscription_four_months_ago(self):
        date_next_subscription = datetime.datetime.fromisoformat('2022-11-19T00:00')
        ret = calc_current_subscription(date_next_subscription)
        self.assertEqual(ret, (datetime.datetime(2022, 7, 19, 0, 0), datetime.datetime(2022, 8, 19, 0, 0)))
