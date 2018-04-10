import datetime
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.backtesthelper import BackTestHelper
from dataaccess.db import YahooEquityDAO
from research.tradesimulation import TradeNode, TradeSimulation


class Momentum(object):

    def __init__(self):
        self.xiv_records = YahooEquityDAO().get_all_equity_price_by_symbol('XIV', from_date_str='2006-07-17')
        self.xiv_values = map(lambda x: x[1], self.xiv_records)

    def condition(self, window):
        result = []
        for i, value in enumerate(self.xiv_values):
            if i < window:
                result.append(True)
            else:
                if value > self.xiv_values[i-window]:
                    result.append(True)
                else:
                    result.append(False)
        return result

    def get_returns(self, window, print_trade_node = False):
        trade_nodes = []
        previous_condition = False
        conditions = self.condition(window)
        dates = map(lambda x: x[0], self.xiv_records)[window:]
        for i in range(len(dates)):
            date = dates[i]
            if conditions[i]:
                if previous_condition is False:
                    # trade_nodes.append(TradeNode('VXX', date, 'sell'))
                    trade_nodes.append(TradeNode('XIV', date, 'buy'))
                    previous_condition = True
            else:
                if previous_condition is True:
                    trade_nodes.append(TradeNode('XIV', date, 'sell'))
                    # trade_nodes.append(TradeNode('VXX', date, 'buy'))
                    previous_condition = False
        returns = list(TradeSimulation.simulate(trade_nodes, dates[0]))
        if print_trade_node:
            for trade_node in trade_nodes:
                print trade_node
            max_draw_down = BackTestHelper.get_max_draw_down(map(lambda x: x[1], returns))
            print 'total return: %s' % returns[-1][1]
            print 'Max drawdown: %s' % max_draw_down
        return returns

    def run1(self):
        returns = self.get_returns(10, True)
        self.plot_for_returns(returns)

    def run(self):
        windows = map(lambda x: x+1, range(99))
        return_values = map(lambda x: self.get_returns(x)[-1][1], windows)
        self.plot(windows, return_values)

    def plot_for_returns(self, returns):
        fig, ax = plt.subplots()
        dates = map(lambda x: x[0], returns)
        values = map(lambda x: x[1], returns)
        ax.plot(dates, values)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(lines[:2], labels[:2])
        plt.show()

    def plot(self, X, Y):
        fig, ax = plt.subplots()
        ax.plot(X, Y)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(lines[:2], labels[:2])
        plt.show()


if __name__ == '__main__':
    Momentum().run1()
    # Momentum().run()




