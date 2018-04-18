import datetime
from utils.listhelper import list_to_hash
from common.tradetime import TradeTime
from dataaccess.history import AbstractHistoricalDataProvider
from datasimulation.montcarlo import MontCarloSimulator


class MontCarloDataProvider(AbstractHistoricalDataProvider):

    def __init__(self):
        self.cache = {}  # consumed in backtest.data
        self._daily_cache = {}
        self._min_cache = {}

    def _generate_historical_daily(self, symbol, window, current_date):
        dates = TradeTime.generate_trade_dates_by_window(window + 1, current_date)
        start_date = dates[0]
        end_date = current_date
        all_dates = TradeTime.generate_dates(start_date, TradeTime.get_latest_trade_date())
        prices = MontCarloSimulator.simulate_daily(symbol, start_date, end_date, len(all_dates), 1)
        rows = map(lambda x, y: [x, y], all_dates, prices[0])
        return rows

    def _generate_hitorical_min(self, symbol, window, current_date_time):
        datetimes = TradeTime.generate_trade_datetimes_by_window(window, current_date_time)
        start = datetimes[0]
        end = datetimes[-1]
        all_datetimes = TradeTime.generate_datetimes(start.date(), end.date())
        prices = MontCarloSimulator.simulate_min(symbol, start, end, len(all_datetimes), 1)
        rows = map(lambda x, y: [x, y], datetimes, prices[0])
        return rows

    def _generate_index_dic(self, rows):
        indexes = range(len(rows))
        time_indexes = map(lambda x, y: [x[0], y], rows, indexes)
        return list_to_hash(time_indexes)

    def history(self, symbol, field, window, current_date):
        if symbol not in self._daily_cache.keys():
            rows = self._generate_historical_daily(symbol, window, current_date)
            self._daily_cache[symbol] = rows
            self._daily_cache['%s_index' % symbol] = self._generate_index_dic(rows)
        indexes_dic = self._daily_cache['%s_index'%symbol]
        index = indexes_dic[current_date]
        return self._daily_cache[symbol][index-window: index]

    # NOTIFICATION: THIS FUNCTION IS NOT TESTED....
    def history_min(self, symbol, window, current_date_time):
        if symbol not in self._min_cache.keys():
            rows = self._generate_hitorical_min(symbol, window, current_date_time)
            self._min_cache[symbol] = rows
            self._min_cache['%s_index' % symbol] = self._generate_index_dic(rows)
        index = self._min_cache['%s_index'%symbol][current_date_time]
        return self._daily_cache[symbol][index-window: index]


if __name__ == '__main__':
    # print MontCarloDataProvider().history('SPY', None, 5, datetime.date.today())
    from utils.timezonehelper import convert_to_us_east_dt
    print MontCarloDataProvider().history_min('SVXY', 390, convert_to_us_east_dt(datetime.datetime.now()))