import datetime
import pandas as pd
import matplotlib.pyplot as plt
from dataaccess.db import YahooEquityDAO
from research.tradesimulation import TradeNode, TradeSimulation


class RollYield(object):

    def __init__(self):
        self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str='2010-12-17')
        self.vxv_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VXV', from_date_str='2010-12-17')
        self.vix_values = map(lambda x: x[1], self.vix_records)
        self.vxv_values = map(lambda x: x[1], self.vxv_records)

    def condition1(self, ma_window):
        vxv_ma = pd.Series(self.vxv_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        vix_ma = pd.Series(self.vix_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x, y: x > y, vxv_ma, vix_ma)

    def condition2(self, ma_window):
        rate = map(lambda x, y: x/y, self.vxv_values, self.vix_values)
        rate_ma = pd.Series(rate).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x: x > 1, rate_ma)

    def get_returns(self, condition, ma_window, vxx_or_tlt='VXX', print_trade_node = False):
        trade_nodes = []
        previous_condition = False
        conditions = condition(ma_window)
        dates = map(lambda x: x[0], self.vix_records)[ma_window:]
        for i in range(len(dates)):
            date = dates[i]
            if conditions[i]:
                if previous_condition is False:
                    trade_nodes.append(TradeNode(vxx_or_tlt, date, 'sell'))
                    trade_nodes.append(TradeNode('XIV', date, 'buy'))
                    previous_condition = True
            else:
                if previous_condition is True:
                    trade_nodes.append(TradeNode('XIV', date, 'sell'))
                    trade_nodes.append(TradeNode(vxx_or_tlt, date, 'buy'))
                    previous_condition = False
        returns = list(TradeSimulation.simulate(trade_nodes, dates[0]))
        if print_trade_node:
            for trade_node in trade_nodes:
                print trade_node
        return returns

    def run(self, ma_window = 7):
        returns1 = self.get_returns(self.condition1, ma_window, 'VXX')
        returns2 = self.get_returns(self.condition2, ma_window, 'TLT')
        self.plot2(returns1, returns2)

    def run1(self, ma_window = 7, print_trade_node=True):
        returns = self.get_returns(self.condition1, ma_window, 'TLT', print_trade_node)
        self.plot(returns)

    def plot(self, returns):
        fig, ax = plt.subplots()
        dates = map(lambda x: x[0], returns)
        values = map(lambda x: x[1], returns)
        ax.plot(dates, values)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(lines[:2], labels[:2])
        plt.show()

    def plot2(self, returns1, returns2):
        dates = map(lambda x: x[0], returns1)
        values1 = map(lambda x: x[1], returns1)
        values2 = map(lambda x: x[1], returns2)
        fig, ax = plt.subplots()
        ax.set_yscale('log')
        ax.plot(dates, values1, 'r-', label='VXX')
        ax.plot(dates, values2, 'b-', label='TLT')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

if __name__ == '__main__':
    RollYield().run1(7)




