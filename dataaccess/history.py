import datetime
import pytz
from abc import ABCMeta, abstractmethod
from utils.logger import Logger, DailyLoggerFactory
from common.pathmgr import PathMgr
from dataaccess.symbols import Symbols
from dataaccess.db import YahooEquityDAO
from common.tradetime import TradeTime
from ibbasic.api import API


def get_logger():
    return DailyLoggerFactory.get_logger(__name__, PathMgr.get_log_path())


class AbstractHistoricalDataProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def history(self, symbol, field, window):
        return None

    @abstractmethod
    def history_min(self, symbol, window):
        return None


class DBProvider(AbstractHistoricalDataProvider):

    def __init__(self):
        pass

    def history(self, symbol, field, window):
        fields_dic = {'open': 'openPrice', 'close': 'adjclosePrice', 'high': 'highPrice', 'low': 'lowPrice',
                      'price': 'adjclosePrice', 'unadj':'closePrice'}
        fields = fields_dic.keys()
        if field.lower() not in field:
            raise Exception('the field should be in %s...'%fields)
        price_field = fields_dic[field]
        yahoo_symbol = Symbols.get_mapped_symbol(symbol, Symbols.YahooSymbolMapping)
        from_date = TradeTime.get_from_date_by_window(window)
        rows = YahooEquityDAO().get_all_equity_price_by_symbol(yahoo_symbol, from_date.strftime('%Y-%m-%d'), price_field)
        return rows

    def history_min(self, symbol, window):
        # yahoo_symbol = Symbols.get_mapped_symbol(symbol, Symbols.YahooSymbolMapping)
        us_dt = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        end_time = datetime.datetime(us_dt.year, us_dt.month, us_dt.day, us_dt.hour, us_dt.minute, us_dt.second)
        days_window = window/391 + 2
        from_date = TradeTime.get_from_date_by_window(days_window)
        start_time = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0)
        rows = YahooEquityDAO().get_min_time_and_price(symbol, start_time, end_time)
        return rows[-window:]


class BackTestDBProvider(AbstractHistoricalDataProvider):

    def __init__(self):
        pass

    def history(self, symbol, field, window, current_date):
        fields_dic = {'open': 'openPrice', 'close': 'adjclosePrice', 'high': 'highPrice', 'low': 'lowPrice',
                      'price': 'adjclosePrice', 'unadj':'closePrice'}
        fields = fields_dic.keys()
        if field.lower() not in field:
            raise Exception('the field should be in %s...'%fields)
        price_field = fields_dic[field]
        yahoo_symbol = Symbols.get_mapped_symbol(symbol, Symbols.YahooSymbolMapping)
        from_date = TradeTime.get_from_date_by_window(window+1, current_date)  # window + 1: get one day more data.
        rows = YahooEquityDAO().get_equity_prices_by_start_end_date(yahoo_symbol, from_date, current_date, price_field)
        return rows[0:window]  # remove current date data.

    def history_min(self, symbol, window, current_date_time):
        # us_dt = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        # end_time = datetime.datetime(us_dt.year, us_dt.month, us_dt.day, us_dt.hour, us_dt.minute, us_dt.second)
        end_time = current_date_time
        days_window = window/391 + 2
        from_date = TradeTime.get_from_date_by_window(days_window, current_date_time.date())
        start_time = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0)
        rows = YahooEquityDAO().get_min_time_and_price(symbol, start_time, end_time)
        return rows[-window:]


class IBProvider(AbstractHistoricalDataProvider):

    def __init__(self):
        self.api = API()

    def history(self, symbol, field, window):
        fields_dic = {'open': 1, 'close': 4, 'high': 2, 'low': 3,
                      'price': 4, 'unadj': 4}
        results = self.api.get_historical_data(symbol, window, 'day')
        return map(lambda x: [x[0], x[fields_dic[field]]], results)

    def history_min(self, symbol, window):
        days_window = window/390 + 1
        records = self.api.get_historical_data(symbol, days_window, 'min')
        results = []
        for record in records[-window:]:
            tradetime = record[0]
            if tradetime.hour == 9 and tradetime.minute == 30 and tradetime.second == 0:
                tradetime = datetime.datetime(tradetime.year, tradetime.month, tradetime.day, 9, 30, 1)
            close = record[4]
            results.append([tradetime, close])
        return results



