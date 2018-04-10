import datetime
import traceback
import pandas as pd
from utils.logger import DailyLoggerFactory
from common.pathmgr import PathMgr
from common.tradetime import TradeTime
from dataaccess.history import DBProvider, IBProvider, BackTestDBProvider
from dataaccess.current import YahooScraper, MarketWatchScraper, IBCurrent


class Data(object):

    def __init__(self):
        # self.historical_data_provider_lst = [IBProvider(), DBProvider()]
        # self.current_data_provider_lst = [IBCurrent(), YahooScraper(), MarketWatchScraper()]
        self.historical_data_provider_lst = [DBProvider(), IBProvider()]
        self.current_data_provider_lst = [YahooScraper(), MarketWatchScraper(), IBCurrent()]

    def get_logger(self):
        return DailyLoggerFactory.get_logger(__name__, PathMgr.get_log_path())

    def _get_history_daily(self, symbol, field, window):
        for provider in self.historical_data_provider_lst:
            try:
                return provider.history(symbol, field, window)
            except Exception as e:
                self.get_logger().error('Trace: ' + traceback.format_exc(), True)
                self.get_logger().error('Error: get historical daily data failed:' + str(e))

    def _get_history_min(self, symbol, window):
        for provider in self.historical_data_provider_lst:
            try:
                return provider.history_min(symbol, window)
            except Exception as e:
                self.get_logger().error('Trace: ' + traceback.format_exc(), True)
                self.get_logger().error('Error: get historical minutes data failed:' + str(e))

    def history(self, assets, field='price', window=30, frequency='1d'):
        """
        get the history data
        :param assets: symbol likes SPX, SPY, VIX, QQQ, etc, or iterable asset
        :param field: support open, close, high, low, price, the price = close
        :param window: the count of records.
        :param frequency: this parameter used for compatible with quantopian algorithm.
        :return:
        """
        if hasattr(assets, '__iter__'):
            results = None
            columns = ['date']
            for symbol in assets:
                columns.append(symbol)
                if frequency == '1d':
                    rows = self._get_history_daily(symbol, field, window)
                elif frequency == '1m':
                    columns[0] = 'minute'
                    rows = self._get_history_min(symbol, window)
                if results is None:
                    results = map(list, rows)
                else:
                    map(lambda x, y: x.append(y[1]), results, rows)
            if len(results) > window:
                results = results[:window]
            df = pd.DataFrame(map(lambda x: x[1:], results), index=map(lambda x: x[0], results), columns=columns[1:])
            return df
        else:
            symbol = str(assets)
            if frequency == '1d':
                rows = self._get_history_daily(symbol, field, window)
            elif frequency == '1m':
                rows = self._get_history_min(symbol, window)
            if len(rows) > window:
                rows = rows[:window]
            series = pd.Series(map(lambda x: x[1], rows), index=map(lambda x: x[0], rows))
            return series

    def current(self, symbols):
        if type(symbols) is str:
            symbols = [symbols]
        prices = None
        for provider in self.current_data_provider_lst:
            prices = provider.get_current_data(symbols)
            if prices is not None:
                break
        if prices is not None:
            if len(symbols) == 1:
                return prices[0]
            elif len(symbols) > 1:
                return pd.Series(prices, index=symbols)
        else:
            return None


class BackTestData(object):

    def __init__(self):
        self.provider = BackTestDBProvider()
        dt = TradeTime.get_latest_trade_date()
        self.specified_date_time = datetime.datetime(dt.year, dt.month, dt.day, 16, 0, 0)

    def set_datetime(self, current_date_time):
        self.specified_date_time = current_date_time

    def history(self, assets, field='price', window=30, frequency='1d'):
        if hasattr(assets, '__iter__'):
            results = None
            columns = ['date']
            for symbol in assets:
                columns.append(symbol)
                if frequency == '1d':
                    rows = self.provider.history(symbol, field, window, self.specified_date_time.date())
                elif frequency == '1m':
                    columns[0] = 'minute'
                    rows = self.provider.history_min(symbol, window, self.specified_date_time)
                if results is None:
                    results = map(list, rows)
                else:
                    map(lambda x, y: x.append(y[1]), results, rows)
            if len(results) > window:
                results = results[:window]
            df = pd.DataFrame(map(lambda x: x[1:], results), index=map(lambda x: x[0], results), columns=columns[1:])
            return df
        else:
            symbol = str(assets)
            if frequency == '1d':
                rows = self.provider.history(symbol, field, window, self.specified_date_time.date())
            elif frequency == '1m':
                rows = self.provider.history_min(symbol, window, self.specified_date_time)
            if len(rows) > window:
                rows = rows[:window]
            series = pd.Series(map(lambda x: x[1], rows), index=map(lambda x: x[0], rows))
            return series

    def current(self, symbols):
        values = self.history(symbols, window=1, frequency='1m')
        if type(symbols) is str:
            return values[0]
        else:
            return values.iloc[0]
if __name__ == '__main__':
    # data = Data()
    # result = data.history(['SPY', 'QQQ'], field='close', window=1)
    # print result
    # print type(result)
    # result = data.history('QQQ', field='close', window=100)
    # print result
    # print result[0]
    # from pandas import Timestamp

    # xiv_prices = data.history('SVXY', "price", 1440, "1m").resample('30T', closed='right',  label='right').last().dropna()
    # xiv_prices.index = [Timestamp(x, tz='US/Eastern') for x in xiv_prices.index]
    # xiv_prices.index = [Timestamp(x, tz='UTC') for x in xiv_prices.index]

    # print xiv_prices
    # print data.history('SPX')
    #print data.history(['SPY', 'VIX'], window=252)
    # print data.current(['SPY', 'QQQ', 'VIX', 'NDX'])
    #print data.current(['SPY', 'QQQ', 'AAPL'])
    #print data.current(['SPY', 'QQQ', 'AAPL', 'NDX'])
    # print data.current(['DJI'])
    #print data.current(['DJI', 'SPY'])
    #print data.current('SPY', ['open', 'close', 'high', 'low'])
    # print data.history(['xiv', 'vxx'], window=1700)
    data = BackTestData()
    data.set_datetime(datetime.datetime(2018, 3, 5, 9, 30, 0))
    # print data.history('SPY', window=5)

    # NOT include current datetime.
    print data.history(['SPY', 'QQQ'], window=5)
    # print data.history('SVXY', window=60, frequency='1m')
    print data.history(['SVXY', 'VIX'], window=60, frequency='1m')
    # print data.history(['SVXY', 'VIX'], window=1, frequency='1m')
    # print data.current('SVXY')
    print data.current(['SVXY', 'VIX'])
    # print Data().current(['SVXY', 'VIX'])
    # print data.history(['SVXY', 'VIX'], window=1, frequency='1m').iloc[0][0]
    # print Data().current(['SVXY', 'VIX'])[0]

