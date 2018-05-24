import datetime
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data import Data
import ffn

class Analysis(object):

    def __init__(self, strategy_name, data):
        self.strategy_name = strategy_name
        self.data = data
        self.trade_trace = []
        self.portfolio_trace = []

    def add_trade_trace(self,  asset, amount, dt):
        # print [dt, asset, amount]
        self.trade_trace.append([dt, asset, amount])

    def add_portfolio_trace(self, dt, portfolio):
        self.portfolio_trace.append([dt, portfolio, portfolio.get_portfolio_value(self.data, True)])

    def get_netliquidations(self):
        return map(lambda x: [x[0], x[2]], self.portfolio_trace)

    def get_returns(self, values=None):
        if values is None:
            values = map(lambda x: x[1], self.get_netliquidations())
        base = values[0]
        return map(lambda x: x/base, values)

    def plot(self):
        dates = map(lambda x: x[0], self.portfolio_trace)
        returns = self.get_returns()
        spy_values = Data().history('SPY', window=len(returns)).values
        bench_mark_returns = self.get_returns(spy_values)
        fig, ax = plt.subplots()
        ax.plot(dates, returns, label=self.strategy_name)
        ax.plot(dates, bench_mark_returns, label='SPY')
        ax.grid()
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def calc_stats(self):
        netliquidations = self.get_netliquidations()
        df = pd.DataFrame(map(lambda x: x[1:], netliquidations), index=map(lambda x: np.datetime64(x[0]), netliquidations), columns=[self.strategy_name])
        df.index.name='Date'
        print df
        perf = df.calc_stats()
        print perf[self.strategy_name].stats


if __name__ == '__main__':
    pass
    # analysis = Analysis('a')
    # print analysis.get_cumulative_return()
    # print analysis.get_annual_return()
    # print analysis.get_max_draw_down()
    # print analysis.get_annual_volatility()
    # print analysis.get_sharpe_ratio()
    # beta = analysis.get_beta()
    # print beta
    # alpha = analysis.get_alpha(beta)
    # print alpha

