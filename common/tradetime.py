import datetime
import pytz

from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, USLaborDay, USThanksgivingDay


class USTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]


class TradeTime(object):

    _holidays_cache = {}
    _special_no_trade_dates = [
        datetime.date(2001, 9, 11),
        datetime.date(2001, 9, 12),
        datetime.date(2001, 9, 13),
        datetime.date(2001, 9, 14),
        datetime.date(2004, 6, 11),
        datetime.date(2007, 1, 2),
        datetime.date(2012, 10, 29),
        datetime.date(2012, 10, 30),
    ]

    def __init__(self):
        pass

    @staticmethod
    def get_trading_close_holidays(year):
        inst = USTradingCalendar()
        return inst.holidays(datetime.datetime(year - 1, 12, 31), datetime.datetime(year, 12, 31))

    @staticmethod
    def is_special_weekday(date, month, week_count, weekday_index):
        if date.month == month and date.weekday() == weekday_index and week_count*7 < date.day < (week_count+1)*7:
            return True

    @staticmethod
    def is_trade_day(date):
        if date in TradeTime._special_no_trade_dates:
            return False
        trading_close_holidays = TradeTime._holidays_cache.get(date.year)
        if trading_close_holidays is None:
            trading_close_holidays = TradeTime.get_trading_close_holidays(date.year)
            TradeTime._holidays_cache[date.year] = trading_close_holidays
        if date.weekday() >= 5:
            return False
        elif date in trading_close_holidays:
            return False
        else:
            return True

    @staticmethod
    def get_half_trade_dates(year):
        '''
        there are 3 special days for half day trading, they are:
        the date before chirstmas day,
        the date before independent day,
        the date after thanks giving day. Oct, the 4th Thursday
        :param nydate:
        :return:
        '''

        half_trade_dates = []

        independent_before_date = datetime.date(year, 7, 3)
        if independent_before_date.weekday() <= 5:
            half_trade_dates.append(independent_before_date)

        nov1 = datetime.date(year, 11, 1)
        delta = 3 - nov1.weekday()
        if delta < 0:
            delta += 7
        thanksgiving_after_date = datetime.date(year, 11, 1 + delta + 3*7 + 1)
        half_trade_dates.append(thanksgiving_after_date)

        christmas_eve = datetime.date(year, 12, 24)
        if christmas_eve.weekday() <= 5:
            half_trade_dates.append(christmas_eve)

        return half_trade_dates

    @staticmethod
    def is_half_trade_day(nydate):
        half_trade_dates = list(TradeTime.get_half_trade_dates(nydate.year))
        return nydate in half_trade_dates

    @staticmethod
    def is_market_open(current_time=None):
        if current_time:
            now = current_time
        else:
            now = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        if TradeTime.is_trade_day(now.date()):
            if TradeTime.is_half_trade_day(now.date()):
                end_hour = 13
            else:
                end_hour = 16
            minutes = now.hour * 60 + now.minute
            if minutes >= 9 * 60 + 30 and minutes < end_hour * 60:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def is_valid_trade_time(specified_time):
        if TradeTime.is_trade_day(specified_time.date()):
            if TradeTime.is_half_trade_day(specified_time.date()):
                end_hour = 13
            else:
                end_hour = 16
            minutes = specified_time.hour * 60 + specified_time.minute
            if 9 * 60 + 30 < minutes <= end_hour * 60:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def get_latest_trade_date():
        for i in range(10):
            trade_date = datetime.datetime.today() - datetime.timedelta(days=i+1)
            if TradeTime.is_trade_day(trade_date.date()):
                return trade_date.date()

    @staticmethod
    def get_from_date_by_window(window, current_date=None):
        if current_date is None:
            current_date = TradeTime.get_latest_trade_date()
        count = 1
        for i in range(2*window+7):
            if count >= window:
                break
            else:
                current_date -= datetime.timedelta(days=1)
                if TradeTime.is_trade_day(current_date):
                    if not TradeTime.is_half_trade_day(current_date):
                        count +=1
        return current_date

    @staticmethod
    def generate_dates(from_date, end_date):
        dates = []
        current_date = from_date
        while current_date <= end_date:
            if TradeTime.is_trade_day(current_date):
                start_date = datetime.date(current_date.year, current_date.month, current_date.day)
                dates.append(start_date)
            current_date += datetime.timedelta(days=1)
        return dates

    @staticmethod
    def generate_trade_dates_by_window(window, end_date):
        count = 0
        dates = []
        current_date = end_date
        while count < window:
            if TradeTime.is_trade_day(current_date):
                dates.append(current_date)
                count = count+1
            current_date = current_date - datetime.timedelta(days=1)
        dates.reverse()
        return dates

    @staticmethod
    def generate_datetimes(from_date, end_date):
        datetimes = []
        current_date = from_date
        while current_date <= end_date:
            if TradeTime.is_trade_day(current_date):
                start_time = datetime.datetime(current_date.year, current_date.month, current_date.day, 9, 31, 0)
                if TradeTime.is_half_trade_day(current_date):
                    count = 180
                else:
                    count = 390
                for i in range(count):
                    datetimes.append(start_time + datetime.timedelta(minutes=i))
            current_date += datetime.timedelta(days=1)
        return datetimes

    @staticmethod
    def generate_trade_datetimes_by_window(window, end_datetime):
        end_date = end_datetime.date()
        date_window = window/390 + 2
        dates = TradeTime.generate_trade_dates_by_window(date_window, end_date)
        datetimes = TradeTime.generate_datetimes(dates[0], dates[-1])
        datetimes = filter(lambda x: x <= end_datetime, datetimes)
        return datetimes[-window-1:]


if __name__ == '__main__':
    #print TradeTime.get_trading_close_holidays(2017)
    print TradeTime.get_half_trade_dates(2017)
    #print TradeTime.is_trade_day(datetime.date(2017, 12, 25))
    #print TradeTime.is_trade_day(datetime.date(2017, 9, 1))
    #print TradeTime.is_trade_day(datetime.date(2017, 9, 4))
    #print TradeTime.is_half_trade_day(datetime.date(2017, 7, 3))
    print TradeTime.is_market_open(datetime.datetime(2017, 12, 26, 15, 15, 0))
    print TradeTime.is_market_open()

    t = datetime.datetime(2017, 11, 6, 15, 15, 0, tzinfo=pytz.timezone('US/Eastern'))
    print t.astimezone(pytz.timezone('US/Eastern'))
    print t.astimezone(pytz.utc)
    print t.astimezone(pytz.timezone('Asia/Shanghai'))
    print datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
    print datetime.datetime.now(tz=pytz.utc)
    print datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
    #n = datetime.datetime.now(tz=pytz.utc)
    #print TradeTime.get_latest_trade_date()
    print TradeTime.get_from_date_by_window(252)
    print TradeTime.get_from_date_by_window(1)
    print '-' * 20
    print TradeTime.generate_trade_dates_by_window(5, datetime.date.today())
    print TradeTime.generate_trade_datetimes_by_window(391, datetime.datetime.now())
