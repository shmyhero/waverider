import unittest
import datetime
from wrapi.time_rules import time_rules


class TimeRulesTest(unittest.TestCase):

    def test_positive_market_open(self):
        self.assertTrue(time_rules.market_open().validate(datetime.datetime(2017, 11, 29, 9, 31, 0)))
        self.assertTrue(time_rules.market_open(1, 0).validate(datetime.datetime(2017, 11, 29, 10, 30, 0)))
        self.assertTrue(time_rules.market_open(1, 0).validate(datetime.datetime(2017, 11, 29, 10, 30, 59)))
        self.assertTrue(time_rules.market_open(minutes=5).validate(datetime.datetime(2017, 11, 29, 9, 35, 0)))
        self.assertTrue(time_rules.market_open(6, 0).validate(datetime.datetime(2017, 11, 29, 15, 30, 0)))

    def test_negative_market_open(self):
        self.assertFalse(time_rules.market_open().validate(datetime.datetime(2017, 11, 29, 9, 30, 0)))
        # Nov 23 is holiday
        self.assertFalse(time_rules.market_open().validate(datetime.datetime(2017, 11, 23, 9, 31, 0)))
        self.assertFalse(time_rules.market_open(1, 0).validate(datetime.datetime(2017, 12, 2, 10, 30, 0)))

    def test_half_day_trade_for_market_open(self):
        self.assertTrue(time_rules.market_open().validate(datetime.datetime(2017, 11, 24, 9, 31, 0)))
        self.assertFalse(time_rules.market_open(6, 0).validate(datetime.datetime(2017, 11, 24, 15, 30, 0)))

    def test_invalid_parameters_in_market_open(self):
        with self.assertRaises(Exception) as context:
            time_rules.market_open(7, 0).validate(datetime.datetime(2017, 11, 29, 16, 30, 0))
            self.assertTrue('Invalid parameters' in context.exception)
        with self.assertRaises(Exception) as context:
            time_rules.market_open(9, 0).validate(datetime.datetime(2017, 11, 29, 18, 30, 0))
            self.assertTrue('Invalid parameters' in context.exception)

    def test_positive_market_close(self):
        self.assertTrue(time_rules.market_close().validate(datetime.datetime(2017, 11, 29, 15, 59, 0)))
        self.assertTrue(time_rules.market_close(minutes=15).validate(datetime.datetime(2017, 11, 29, 15, 45, 0)))
        self.assertTrue(time_rules.market_close(hours=1, minutes=15).validate(datetime.datetime(2017, 11, 29, 14, 45, 0)))
        self.assertTrue(time_rules.market_close(hours=5, minutes=30).validate(datetime.datetime(2017, 11, 29, 10, 30, 0)))

    def test_negative_market_close(self):
        self.assertFalse(time_rules.market_close().validate(datetime.datetime(2017, 11, 29, 16, 0, 0)))
        self.assertFalse(time_rules.market_close().validate(datetime.datetime(2017, 11, 23, 15, 59, 0)))
        self.assertFalse(time_rules.market_close(1, 0).validate(datetime.datetime(2017, 12, 2, 15, 0, 0)))

    def test_half_day_trade_for_market_close(self):
        self.assertTrue(time_rules.market_close().validate(datetime.datetime(2017, 11, 24, 12, 59, 0)))
        self.assertTrue(time_rules.market_close(1, 0).validate(datetime.datetime(2017, 11, 24, 12, 0, 0)))
        self.assertFalse(time_rules.market_close(minutes=15).validate(datetime.datetime(2017, 11, 24, 15, 45, 0)))

    def test_invalid_parameters_in_market_close(self):
        with self.assertRaises(Exception) as context:
            time_rules.market_close(7, 0).validate(datetime.datetime(2017, 11, 29, 9, 0, 0))
            self.assertTrue('Invalid parameters' in context.exception)
        with self.assertRaises(Exception) as context:
            time_rules.market_close(9, 0).validate(datetime.datetime(2017, 11, 29, 7, 0, 0))
            self.assertTrue('Invalid parameters' in context.exception)



