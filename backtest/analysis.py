import datetime
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
        self.portfolio_trace.append([dt, portfolio, portfolio.get_portfolio_value(self.data, False)])

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
        spy_values = self.data.history('SPY', window=len(returns)).values
        bench_mark_returns = self.get_returns(spy_values)
        fig, ax = plt.subplots()
        ax.plot(dates, returns, label=self.strategy_name)
        ax.plot(dates, bench_mark_returns, label='SPY')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def calc_stats(self):
        netliquidations = self.get_netliquidations()
        df = pd.DataFrame(map(lambda x: x[1:], netliquidations), index=map(lambda x: np.datetime64(x[0]), netliquidations), columns=[self.strategy_name])
        df.index.name='Date'
        print df
        perf = df.calc_stats()
        print perf[self.strategy_name].stats

    def get_start_date(self):
        return self.portfolio_trace[0][0]

    def get_end_date(self):
        return self.portfolio_trace[-1][0]

    def get_total_month(self):
        return self.get_end_date().month - self.get_start_date().month

    def get_cumulative_return(self, returns=None):
        if returns is None:
            returns = self.get_returns()
        return returns[-1] -1

    def get_annual_return(self, returns=None):
        cumulative_return = self.get_cumulative_return(returns)
        days = (self.get_end_date() - self.get_start_date()).days
        return pow(1+cumulative_return, 252.0/days)-1

    def get_annual_volatility(self):
        values = map(lambda x: x[1], self.net_liquidations)
        return math.sqrt(252) * np.std(np.diff(np.log(values)))

    def get_sharpe_ratio(self):
        values = map(lambda x: x-1, self.get_returns())
        return np.mean(values) / np.std(np.diff(values))

    def get_max_draw_down(self):
        max_value = -1
        max_draw_down = 0
        from_date = None
        end_date = None
        for [date, value] in self.net_liquidations:
            if value > max_value:
                max_value = value
                from_date = date
            else:
                draw_down = (max_value - value*1.0)/max_value
                if draw_down > max_draw_down:
                    max_draw_down = draw_down
                    end_date = date
        return [max_draw_down, from_date, end_date]

    def get_beta(self):
        covariance = np.cov(self.bench_mark_returns, self.returns)
        beta = covariance[0, 1] / covariance[1, 1]
        return beta

    def get_alpha(self, beta):
        if beta is None:
            beta = self.get_beta()
        bench_mark_annual_return = self.get_annual_return(self.bench_mark_returns)
        return (self.get_annual_return()+1)/(+ bench_mark_annual_return + 1)/beta


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

