import traceback
import pandas as pd
from utils.logger import Logger
from common.pathmgr import PathMgr
from dataaccess.history import DBProvider, IBProvider
from dataaccess.current import YahooScraper, MarketWatchScraper, IBCurrent


class Data(object):

    def __init__(self):
        self.logger = Logger(__name__, PathMgr.get_log_path())
        # self.historical_data_provider_lst = [IBProvider(), DBProvider()]
        # self.current_data_provider_lst = [IBCurrent(), YahooScraper(), MarketWatchScraper()]
        self.historical_data_provider_lst = [DBProvider(), IBProvider()]
        self.current_data_provider_lst = [YahooScraper(), MarketWatchScraper(), IBCurrent()]

    def _get_history_daily(self, symbol, field, window):
        for provider in self.historical_data_provider_lst:
            try:
                return provider.history(symbol, field, window)
            except Exception as e:
                self.logger.error('Trace: ' + traceback.format_exc(), True)
                self.logger.error('Error: get current price from Yahoo failed:' + str(e))

    def _get_history_min(self, symbol, window):
        for provider in self.historical_data_provider_lst:
            try:
                return provider.history_min(symbol, window)
            except Exception as e:
                self.logger.error('Trace: ' + traceback.format_exc(), True)
                self.logger.error('Error: get current price from Yahoo failed:' + str(e))


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


if __name__ == '__main__':
    data = Data()
    # result = data.history(['SPY', 'QQQ'], field='close', window=1)
    # print result
    # print type(result)
    # result = data.history('QQQ', field='close', window=100)
    # print result
    # print result[0]
    from pandas import Timestamp

    xiv_prices = data.history('SVXY', "price", 1440, "1m").resample('30T',
                                                                         closed='right',
                                                                         label='right').last().dropna()
    xiv_prices.index = [Timestamp(x, tz='US/Eastern') for x in xiv_prices.index]
    xiv_prices.index = [Timestamp(x, tz='UTC') for x in xiv_prices.index]

    print xiv_prices
    # print data.history('SPX')
    #print data.history(['SPY', 'VIX'], window=252)
    # print data.current(['SPY', 'QQQ', 'VIX', 'NDX'])
    #print data.current(['SPY', 'QQQ', 'AAPL'])
    #print data.current(['SPY', 'QQQ', 'AAPL', 'NDX'])
    # print data.current(['DJI'])
    #print data.current(['DJI', 'SPY'])
    #print data.current('SPY', ['open', 'close', 'high', 'low'])
    # print data.history(['xiv', 'vxx'], window=1700)
