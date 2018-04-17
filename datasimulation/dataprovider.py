import datetime
from common.tradetime import TradeTime
from dataaccess.history import AbstractHistoricalDataProvider
from datasimulation.montcarlo import MontCarloSimulator


class MontCarloDataProvider(AbstractHistoricalDataProvider):

    def __init__(self):
        pass

    def history(self, symbol, field, window, current_date):
        start_date = TradeTime.get_from_date_by_window(window+1, current_date)  # window + 1: get one day more data.
        end_date = current_date
        prices = MontCarloSimulator.simulate_daily(symbol, start_date, end_date, window+1, 1)
        dates = TradeTime.generate_trade_dates_by_window(window + 1, current_date)
        rows = map(lambda x, y: [x, y], dates, prices[0])
        return rows[0:window]  # remove current date data.

    def history_min(self, symbol, window, current_date_time):
        #TODO: TradeTime.generate_trade_datetimes_by_window()....
        pass
        # # us_dt = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        # # end_time = datetime.datetime(us_dt.year, us_dt.month, us_dt.day, us_dt.hour, us_dt.minute, us_dt.second)
        # end_time = current_date_time
        # days_window = window/391 + 2
        # from_date = TradeTime.get_from_date_by_window(days_window, current_date_time.date())
        # start_time = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0)
        # rows = YahooEquityDAO().get_min_time_and_price(symbol, start_time, end_time)
        # return rows[-window:]

if __name__ == '__main__':
    print MontCarloDataProvider().history('SPY', None, 5, datetime.date.today())