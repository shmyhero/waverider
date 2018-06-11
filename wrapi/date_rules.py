from abc import abstractmethod
from datetime import datetime, timedelta
from common.tradetime import TradeTime


class DateRule(object):

    @abstractmethod
    def validate(self, date):
        pass

    @staticmethod
    def offset_days(current_date, days_offset):
        count = 0
        date = current_date
        while count < abs(days_offset):
            if days_offset > 0:
                date += timedelta(days=1)
            else:
                date -= timedelta(days=1)
            if TradeTime.is_trade_day(date):
                count += 1
        return date


class EveryDayRule(DateRule):

    def validate(self, date):
        return TradeTime.is_trade_day(date)


class WeekStartRule(DateRule):

    def __init__(self, days_offset=0):
        self.days_offset = days_offset

    @staticmethod
    def is_week_start_date(date):
        if not TradeTime.is_trade_day(date):
            return False
        weekday = date.weekday()
        # if find any date before this day is trade day, return False.
        for i in range(weekday):
            date_i = date - timedelta(i+1)
            if TradeTime.is_trade_day(date_i):
                return False
        return True

    def validate(self, date):
        if TradeTime.is_trade_day(date):
            week_start_date = DateRule.offset_days(date, -self.days_offset)
            return self.is_week_start_date(week_start_date)
        else:
            return False


class WeekEndRule(DateRule):

    def __init__(self, days_offset=0):
        self.days_offset = days_offset

    @staticmethod
    def is_week_end_date(date):
        if not TradeTime.is_trade_day(date):
            return False
        left_days = 4 - date.weekday()
        # if find any date after this day is trade day, return False.
        for i in range(left_days):
            date_i = date + timedelta(i + 1)
            if TradeTime.is_trade_day(date_i):
                return False
        return True

    def validate(self, date):
        if TradeTime.is_trade_day(date):
            week_end_date = DateRule.offset_days(date, self.days_offset)
            return self.is_week_end_date(week_end_date)
        else:
            return False


class MonthStartRule(DateRule):

    def __init__(self, days_offset=0):
        self.days_offset = days_offset

    @staticmethod
    def is_month_start_date(date):
        if not TradeTime.is_trade_day(date):
            return False
        # if find any date before this day is trade day, return False.
        for i in range(date.day-1):
            date_i = date - timedelta(i + 1)
            if TradeTime.is_trade_day(date_i):
                return False
        return True

    def validate(self, date):
        if TradeTime.is_trade_day(date):
            month_start_date = DateRule.offset_days(date, -self.days_offset)
            return MonthStartRule.is_month_start_date(month_start_date)
        else:
            return False


class MonthEndRule(DateRule):

    def __init__(self, days_offset=0):
        self.days_offset = days_offset

    @staticmethod
    def is_month_end_date(date):
        if not TradeTime.is_trade_day(date):
            return False
        next_month = date.replace(day=28) + timedelta(days=4)
        last_date = next_month - timedelta(days=next_month.day)
        left_days = last_date.day - date.day
        # if find any date after this day is trade day, return False.
        for i in range(left_days):
            date_i = date + timedelta(i + 1)
            if TradeTime.is_trade_day(date_i):
                return False
        return True

    def validate(self, date):
        if TradeTime.is_trade_day(date):
            month_end_date = DateRule.offset_days(date, self.days_offset)
            return MonthEndRule.is_month_end_date(month_end_date)
        else:
            return False



