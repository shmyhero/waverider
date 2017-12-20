from abc import abstractmethod, ABCMeta
from common.tradetime import TradeTime


class TimeRule(object):

    @abstractmethod
    def validate(self, dt):
        pass

    @staticmethod
    def check_parameters(hours, minutes):
        if hours * 60 + minutes >= 6 * 60 + 30:
            raise Exception('Invalid parameters')


class MarketOpenRule(TimeRule):

    def __init__(self, hours=0, minutes=1):
        TimeRule.check_parameters(hours, minutes)
        self.hours = hours
        self.minutes = minutes

    def validate(self, dt):
        if TradeTime.is_trade_day(dt.date()):
            if TradeTime.is_half_trade_day(dt.date()) and self.hours * 60 + self.minutes >= 3*60 + 30:
                return False
            else:
                passed_minutes = dt.hour * 60 + dt.minute - (9*60 + 30)
                if passed_minutes == self.hours * 60 + self.minutes:
                    return True
                else:
                    return False
        return False


class MarketCloseRule(TimeRule):

    def __init__(self, hours=0, minutes=1):
        TimeRule.check_parameters(hours, minutes)
        self.hours = hours
        self.minutes = minutes

    def validate(self, dt):
        if TradeTime.is_trade_day(dt.date()):
            if TradeTime.is_half_trade_day(dt.date()):
                if self.hours * 60 + self.minutes >= 3.5*60:
                    return False
                else:
                    left_minutes = 13 * 60 - (dt.hour * 60 + dt.minute)
                    if left_minutes == self.hours * 60 + self.minutes:
                        return True
                    else:
                        return False

            else:
                left_minutes = 16 * 60 - (dt.hour * 60 + dt.minute)
                if left_minutes == self.hours * 60 + self.minutes:
                    return True
                else:
                    return False
        return False
