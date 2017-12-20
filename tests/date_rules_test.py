import unittest
import datetime
from wrapi.quantopian import date_rules


class DateRulesTest(unittest.TestCase):

    def test_every_day(self):
        self.assertTrue(date_rules.every_day().validate(datetime.date(2017, 11, 29)))
        self.assertFalse(date_rules.every_day().validate(datetime.date(2017, 11, 23)))
        self.assertFalse(date_rules.every_day().validate(datetime.date(2017, 11, 25)))

    def test_week_start(self):
        self.assertTrue(date_rules.week_start().validate(datetime.date(2017, 11, 27)))
        self.assertTrue(date_rules.week_start(days_offset=1).validate(datetime.date(2017, 11, 28)))
        self.assertTrue(date_rules.week_start(days_offset=3).validate(datetime.date(2017, 11, 30)))
        self.assertTrue(date_rules.week_start(days_offset=-1).validate(datetime.date(2017, 11, 24)))
        self.assertTrue(date_rules.week_start(days_offset=-2).validate(datetime.date(2017, 11, 22)))
        self.assertFalse(date_rules.week_start(days_offset=-2).validate(datetime.date(2017, 11, 23)))

    def test_week_end(self):
        self.assertTrue(date_rules.week_end().validate(datetime.date(2017, 11, 24)))
        self.assertTrue(date_rules.week_end(-1).validate(datetime.date(2017, 11, 22)))
        self.assertTrue(date_rules.week_end(+1).validate(datetime.date(2017, 11, 27)))

    def test_month_start(self):
        self.assertTrue(date_rules.month_start().validate(datetime.date(2017, 11, 1)))
        self.assertFalse(date_rules.month_start().validate(datetime.date(2017, 10, 1)))
        self.assertTrue(date_rules.month_start(1).validate(datetime.date(2017, 11, 2)))
        self.assertTrue(date_rules.month_start(7).validate(datetime.date(2017, 11, 10)))
        self.assertTrue(date_rules.month_start(-1).validate(datetime.date(2017, 11, 30)))

    def test_month_end(self):
        self.assertTrue(date_rules.month_end().validate(datetime.date(2017, 11, 30)))
        self.assertTrue(date_rules.month_end().validate(datetime.date(2017, 10, 31)))
        self.assertFalse(date_rules.month_end().validate(datetime.date(2017, 9, 30)))
        self.assertTrue(date_rules.month_end().validate(datetime.date(2017, 9, 29)))
        self.assertTrue(date_rules.month_end(-1).validate(datetime.date(2017, 9, 28)))
        self.assertTrue(date_rules.month_end(2).validate(datetime.date(2017, 10, 3)))


