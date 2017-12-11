import pandas as pd
from dataaccess.history import DBProvider
from dataaccess.webscraper import  MarketWatchScraper


class Data(object):

    def __init__(self):
        self.historical_data_provider = DBProvider()
        self.current_data_provider = MarketWatchScraper()

    def history(self, assets, field='price', window=30, frequency='1d'):
        """
        get the history data
        :param assets: symbol likes SPX, SPY, VIX, QQQ, etc, or iterable asset
        :param field: support open, close, high, low, price, the price = close
        :param window: the count of records.
        :param frequency: this parameter used for compatible with quantopian algorithm.
        :return:
        """
        frequency = '1d'
        if hasattr(assets, '__iter__'):
            results = None
            columns = ['date']
            for symbol in assets:
                columns.append(symbol)
                rows = self.historical_data_provider.history(symbol, field, window)
                if results is None:
                    results = map(list, rows)
                else:
                    map(lambda x, y: x.append(y[1]), results, rows)
            df = pd.DataFrame(map(lambda x: x[1:], results), index=map(lambda x: x[0], results), columns=columns[1:])
            return df
        else:
            symbol = str(assets)
            rows = self.historical_data_provider.history(symbol, field, window)
            df = pd.DataFrame(map(lambda x: x[1:], rows), index=map(lambda x: x[0], rows), columns = ['price'])
            return df

    def current(self, symbols, fields=['price']):
        if type(symbols) is str:
            symbols = [symbols]
        if type(fields) is str:
            fields = [fields]
        field_dic = {'open': 0, 'close': 1, 'price': 1, 'high': 2, 'low': 3, 'volume': 4, 'contract': 5}
        indexes = map(lambda x: field_dic[x],fields)
        records = self.current_data_provider.get_current_data(symbols)
        if len(symbols) == 1 and len(fields) == 1:
            return records[0][0]
        elif len(symbols) > 1 and len(fields) == 1:
            values = map(lambda x: x[indexes[0]], records)
            return pd.Series(values, index=symbols)
        elif len(symbols) == 1 and len(fields) >= 1:
            values = map(lambda index: records[0][index], indexes)
            return pd.Series(values, index=fields)
        else:
            rows = map(lambda record: map(lambda index: record[index], indexes), records)
            df = pd.DataFrame(rows, columns=fields, index=symbols)
            return df


if __name__ == '__main__':
    data = Data()
    #print data.history('QQQ', field='close', window=100)
    #print data.history('SPX')
    #print data.history(['SPY', 'VIX'], window=252)
    #print data.current(['SPY', 'QQQ', 'VIX', 'NDX'], ['price', 'volume'])
    #print data.current(['SPY', 'QQQ', 'AAPL'], ['price', 'open', 'high', 'low', 'close', 'volume'])
    #print data.current(['SPY', 'QQQ', 'AAPL', 'NDX'], ['price', 'open', 'high', 'low', 'close'])
    #print data.current(['DJI'], ['price', 'open', 'high', 'low', 'close', 'volume'])
    #print data.current(['DJI', 'SPY'], 'price')
    print data.current('SPY', ['open', 'close', 'high', 'low'])
