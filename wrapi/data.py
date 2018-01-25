import pandas as pd
from utils.logger import Logger
from common.pathmgr import PathMgr
from dataaccess.history import DBProvider
from dataaccess.webscraper import YahooScraper, MarketWatchScraper


class Data(object):

    def __init__(self):
        self.logger = Logger(__name__, PathMgr.get_log_path())
        self.historical_data_provider = DBProvider()
        self.current_data_provider_lst = [YahooScraper(), MarketWatchScraper()]

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
                if frequency == 'id':
                    rows = self.historical_data_provider.history(symbol, field, window)
                elif frequency == '1m':
                    columns[0] = 'minute'
                    rows = self.historical_data_provider.history_min(symbol, window)
                if results is None:
                    results = map(list, rows)
                else:
                    map(lambda x, y: x.append(y[1]), results, rows)
            df = pd.DataFrame(map(lambda x: x[1:], results), index=map(lambda x: x[0], results), columns=columns[1:])
            return df
        else:
            symbol = str(assets)
            if frequency == 'id':
                rows = self.historical_data_provider.history(symbol, field, window)
            elif frequency == '1m':
                rows = self.historical_data_provider.history_min(symbol, window)
            df = pd.DataFrame(map(lambda x: x[1:], rows), index=map(lambda x: x[0], rows), columns = ['price'])
            return df

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
    # print data.history('QQQ', field='close', window=100)
    print data.history('XIV', window=1000, frequency='1m')
    # print data.history('SPX')
    #print data.history(['SPY', 'VIX'], window=252)
    # print data.current(['SPY', 'QQQ', 'VIX', 'NDX'])
    #print data.current(['SPY', 'QQQ', 'AAPL'])
    #print data.current(['SPY', 'QQQ', 'AAPL', 'NDX'])
    # print data.current(['DJI'])
    #print data.current(['DJI', 'SPY'])
    #print data.current('SPY', ['open', 'close', 'high', 'low'])
    # print data.history(['xiv', 'vxx'], window=1700)
