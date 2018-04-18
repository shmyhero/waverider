import datetime
import pandas as pd
from utils.listhelper import list_to_hash
from common.tradetime import TradeTime
from dataaccess.history import BackTestDBProvider


class Data(object):

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

    def get_market_price(self, symbol):
        try:
            market_price = self.current(symbol)
        except Exception:
            market_price = self.history(symbol, window=1)[0]
        return market_price

    def get_daily_price(self, symbol):
        # return self.history(symbol, window=1)[0]
        date = self.specified_date_time.date()
        if symbol in self.provider.cache.keys() and date >= self.provider.cache[symbol][0]:
            dic = self.provider.cache[symbol][1]
            return dic[date]
        else:
            window = len(TradeTime.generate_dates(date, TradeTime.get_latest_trade_date()))
            rows = self.provider.history(symbol, 'price', window, TradeTime.get_latest_trade_date())
            dic = list_to_hash(rows)
            self.provider.cache[symbol] = [rows[0][0], dic]
            return dic[date]



if __name__ == '__main__':
    data = Data()
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
