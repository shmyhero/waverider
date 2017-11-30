import unittest
import datetime
from wrapi.date_rules import date_rules


class DateRulesTest(unittest.TestCase):

    def test_every_day(self):
        self.assertTrue(date_rules.everyday().validate(datetime.date(2017, 11, 29)))
        self.assertFalse(date_rules.everyday().validate(datetime.date(2017, 11, 23)))
        self.assertFalse(date_rules.everyday().validate(datetime.date(2017, 11, 25)))

