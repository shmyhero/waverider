import datetime
import math
import numpy as np
import pandas as pd
from dataaccess.db import YahooEquityDAO
import matplotlib.pyplot as plt


class MontCarlo(object):

    def __init__(self, prices):
        self.prices = prices

    def brownian_motion(self, window, times):
        returns = self.prices.pct_change()
        last_price = self.prices[-1]
        result = []

        # Create Each Simulation as a Column in df
        for x in range(times):
            # Inputs
            count = 0
            avg_daily_ret = returns.mean()
            variance = returns.var()

            daily_vol = returns.std()
            daily_drift = avg_daily_ret - (variance / 2)
            drift = daily_drift - 0.5 * daily_vol ** 2

            # Append Start Value
            prices = []

            shock = drift + daily_vol * np.random.normal()
            last_price * math.exp(shock)
            prices.append(last_price)

            for i in range(window):
                if count == 251:
                    break
                shock = drift + daily_vol * np.random.normal()
                price = prices[count] * math.exp(shock)
                prices.append(price)

                count += 1
            result.append(prices)
        return result

    def brownian_motion2(self, window, times):
        last_price = self.prices[-1]

        # calculate the compound annual growth rate(CAGR) which
        # will give us mean return input(mu)
        days = len(self.prices)
        cagr = ((last_price / self.prices[0]) ** (365.0 / days)) - 1
        mu = cagr

        returns = self.prices.pct_change()
        vol = returns.std() * math.sqrt(252)
        results = []
        for i in range(times):
            daily_returns = np.random.normal((1 + mu) ** (1 / window), vol / math.sqrt(window), window)
            price_list = [last_price]
            for x in daily_returns:
                price_list.append(price_list[-1] * x)
            results.append(price_list)
        return results


def simulate_min(symbol, start, end, window, times):
    rows = YahooEquityDAO().get_min_time_and_price(symbol, start, end)
    prices = pd.Series(map(lambda x: x[1], rows), index=map(lambda x: x[0], rows))
    return MontCarlo(prices).brownian_motion2(window, times)

def simulate_daily(symbol, start, end, window, times):
    rows = YahooEquityDAO().get_equity_prices_by_start_end_date(symbol, start, end)
    prices = pd.Series(map(lambda x: x[1], rows), index=map(lambda x: x[0], rows))
    return MontCarlo(prices).brownian_motion2(window, times)


def line_graph(results):
    for result in results:
        plt.plot(result)
    plt.show()


if __name__ == '__main__':
    results = simulate_min('SVXY', datetime.datetime(2018, 2, 7, 0, 0, 0), datetime.datetime(2018, 4, 1, 0, 0, 0), 500, 5)
    # results = simulate_min('SPY', datetime.datetime(2001, 2, 7, 0, 0, 0), datetime.datetime(2018, 4, 1, 0, 0, 0), 500, 5)
    line_graph(results)
