import datetime
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.backtesthelper import BackTestHelper
from dataaccess.db import YahooEquityDAO
from research.tradesimulation import TradeNode, TradeSimulation


class RollYieldMomentum(object):

    def __init__(self):
        self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str='2006-07-17')
        self.vxv_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VXV', from_date_str='2006-07-17')
        # self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str='2010-01-01')
        # self.vxv_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VXV', from_date_str='2010-01-01')
        self.vix_values = map(lambda x: x[1], self.vix_records)
        self.vxv_values = map(lambda x: x[1], self.vxv_records)
        self.xiv_records = YahooEquityDAO().get_all_equity_price_by_symbol('XIV', from_date_str='2006-07-17')
        self.xiv_values = map(lambda x: x[1], self.xiv_records)
        self.vxx_records = YahooEquityDAO().get_all_equity_price_by_symbol('VXX', from_date_str='2006-07-17')
        self.vxx_values = map(lambda x: x[1], self.vxx_records)

    def condition_roll_yield(self, ma_window):
        vxv_ma = pd.Series(self.vxv_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        vix_ma = pd.Series(self.vix_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        # return map(lambda x, y: x > y*0.99, vxv_ma, vix_ma)
        return map(lambda x, y: x > y, vxv_ma, vix_ma)

    def condition_roll_yield2(self, ma_window):
        rate = map(lambda x, y: x/y, self.vxv_values, self.vix_values)
        rate_ma = pd.Series(rate).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x: x > 1, rate_ma)

    def condition_momentum(self, symbol,  momentum_window=10):
        records = YahooEquityDAO().get_all_equity_price_by_symbol(symbol, from_date_str='2006-07-17')
        values = map(lambda x: x[1], records)
        result = []
        for i, value in enumerate(values):
            if i < momentum_window:
                result.append(True)
            else:
                if value > values[i - momentum_window]:
                    result.append(True)
                else:
                    result.append(False)
        return result

    def get_returns(self, ma_window=7, momentum_window=10, print_trade_node = False):
        trade_nodes = []
        hold_xiv = False
        hold_vxx = False
        roll_yield_conditions = self.condition_roll_yield(ma_window)
        momentum_xiv_conditions = self.condition_momentum('XIV', momentum_window)[ma_window:]
        # momentum_vxx_conditions = self.condition_momentum('VXX', momentum_window)[ma_window:]
        dates = map(lambda x: x[0], self.vix_records)[ma_window:]
        for i in range(len(dates)):
            date = dates[i]
            if roll_yield_conditions[i]:
                if hold_vxx:
                    trade_nodes.append(TradeNode('VXX', date, 'sell'))
                    hold_vxx = False
                # if hold_xiv is False:
                #     trade_nodes.append(TradeNode('XIV', date, 'buy'))
                #     hold_xiv = True
                if momentum_xiv_conditions[i]:
                    if hold_xiv is False:
                        trade_nodes.append(TradeNode('XIV', date, 'buy'))
                        hold_xiv = True
                else:
                    if hold_xiv:
                        trade_nodes.append(TradeNode('XIV', date, 'sell'))
                        hold_xiv = False
            else:
                if hold_xiv is True:
                    trade_nodes.append(TradeNode('XIV', date, 'sell'))
                    hold_xiv = False
                if not hold_vxx:
                    trade_nodes.append(TradeNode('VXX', date, 'buy'))
                    hold_vxx = True


        returns = list(TradeSimulation.simulate(trade_nodes, dates[0]))
        if print_trade_node:
            for trade_node in trade_nodes:
                print trade_node
            max_draw_down = BackTestHelper.get_max_draw_down(map(lambda x: x[1], returns))
            print 'total return: %s' % returns[-1][1]
            print 'Max drawdown: %s' % max_draw_down
        return returns

    def run1(self, ma_window=7, momentum_window=10, print_trade_node=True):
        returns = self.get_returns(ma_window, momentum_window, print_trade_node)
        self.plot_for_returns(returns)

    def plot_for_returns(self, returns):
        fig, ax = plt.subplots()
        dates = map(lambda x: x[0], returns)
        values = map(lambda x: x[1], returns)
        ax.plot(dates, values)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(lines[:2], labels[:2])
        plt.show()

    def run(self, ma_window=7):
        windows = map(lambda x: x+1, range(199))
        return_values = map(lambda x: self.get_returns(ma_window, x)[-1][1], windows)
        self.plot(windows, return_values)

    def plot(self, X, Y):
        fig, ax = plt.subplots()
        ax.plot(X, Y)
        lines, labels = ax.get_legend_handles_labels()
        ax.legend(lines[:2], labels[:2])
        plt.show()



if __name__ == '__main__':
    # RollYieldMomentum().run1(7, 10)
    # RollYieldMomentum().run()
    RollYieldMomentum().run1(7, 81)




