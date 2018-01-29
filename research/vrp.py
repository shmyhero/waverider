import datetime
import pandas as pd
import matplotlib.pyplot as plt
from utils.optioncalculator import OptionCalculator
from dataaccess.db import YahooEquityDAO
from research.tradesimulation import TradeNode, TradeSimulation


class VRP(object):

    """Volatility risk premium """
    def __init__(self, vol_circle=10):
        from_date_str = '2006-07-17'
        spy_records = YahooEquityDAO().get_all_equity_price_by_symbol('SPY', from_date_str)
        self.vol_list = OptionCalculator.get_year_history_volatility_list(spy_records, vol_circle)
        self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str)[vol_circle:]
        self.vol_values = map(lambda x: x[1]*100, self.vol_list)
        self.vix_values = map(lambda x: x[1], self.vix_records)

    def condition1(self, ma_window):
        vol_ma = pd.Series(self.vol_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        vix_ma = pd.Series(self.vix_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x, y: x > y, vix_ma, vol_ma)

    def condition2(self, ma_window):
        delta_list = map(lambda x, y: x-y, self.vix_values, self.vol_values)
        ma_delta_list = pd.Series(delta_list).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x: x > 0, ma_delta_list)

    def get_returns(self, condition, ma_window):
        trade_nodes = []
        previous_condition = False
        conditions = condition(ma_window)
        dates = map(lambda x: x[0], self.vix_records)[ma_window:]
        for i in range(len(dates)):
            date = dates[i]
            if conditions[i]:
                if previous_condition is False:
                    trade_nodes.append(TradeNode('VXX', date, 'sell'))
                    trade_nodes.append(TradeNode('XIV', date, 'buy'))
                    previous_condition = True
            else:
                if previous_condition is True:
                    trade_nodes.append(TradeNode('XIV', date, 'sell'))
                    trade_nodes.append(TradeNode('VXX', date, 'buy'))
                    previous_condition = False
        returns = list(TradeSimulation.simulate(trade_nodes, dates[0]))
        for trade_node in trade_nodes:
           print trade_node
        return returns

    def plot(self, returns):
        fig, ax = plt.subplots()
        dates = map(lambda x: x[0], returns)
        values = map(lambda x: x[1], returns)
        ax.plot(dates, values)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(lines[:2], labels[:2])
        plt.show()

    def plot2(self, returns1, returns2, ma_window):
        dates = map(lambda x: x[0], returns1)
        values1 = map(lambda x: x[1], returns1)
        values2 = map(lambda x: x[1], returns2)
        fig, ax = plt.subplots()
        # ax.set_yscale('log')
        ax.plot(dates, values1, 'r-', label='ma%s_divide'%ma_window)
        ax.plot(dates, values2, 'b-', label='divide_ma%s'%ma_window)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def run(self, ma_window = 5):
        returns = self.get_returns(self.condition2, ma_window)
        self.plot(returns)

    def run2(self, ma_window = 5):
        returns1 = self.get_returns(self.condition1, ma_window)
        returns2 = self.get_returns(self.condition2, ma_window)
        self.plot2(returns1, returns2, ma_window)


if __name__ == '__main__':
    #VRP(10).run(8)
    VRP().run(8)


