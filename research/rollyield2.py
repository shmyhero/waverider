import datetime
import pandas as pd
import matplotlib.pyplot as plt
from dataaccess.db import YahooEquityDAO
from research.tradesimulation import TradeNode, TradeSimulation


class RollYield(object):

    def __init__(self):
        self.spy_monthly_records = YahooEquityDAO().get_equity_monthly_price_by_symbol('SPY')
        self.spy_monthly_indicator = self.get_spy_monthly_indicator()
        self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str='2010-12-17')
        self.vxv_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VXV', from_date_str='2010-12-17')
        self.vix_values = map(lambda x: x[1], self.vix_records)
        self.vxv_values = map(lambda x: x[1], self.vxv_records)

    def bull_market_p(self, date):
        bull_p = False
        for [monthly_date, value] in self.spy_monthly_indicator:
            if monthly_date > date:
                break
            else:
                bull_p = value
        return bull_p

    def get_spy_monthly_indicator(self):
        ma_monthly_window = 8
        spy_values = map(lambda x: x[1], self.spy_monthly_records)
        spy_ma = pd.Series(spy_values).rolling(window=ma_monthly_window).mean().tolist()[ma_monthly_window:]
        return map(lambda x, y: [x[0], x[1] > y], self.spy_monthly_records[ma_monthly_window:], spy_ma)


    def condition1(self, ma_window):
        vxv_ma = pd.Series(self.vxv_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        vix_ma = pd.Series(self.vix_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x, y: x > y, vxv_ma, vix_ma)

    def condition2(self, ma_window):
        rate = map(lambda x, y: x/y, self.vxv_values, self.vix_values)
        rate_ma = pd.Series(rate).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x: x > 1, rate_ma)

    def get_returns(self, condition, ma_window, print_trade_node = False):
        trade_nodes = []
        hold_xiv = False
        hold_vxx = False
        conditions = condition(ma_window)
        dates = map(lambda x: x[0], self.vix_records)[ma_window:]
        for i in range(len(dates)):
            date = dates[i]
            long_vix = conditions[i]
            if long_vix:
                if hold_vxx:
                    trade_nodes.append(TradeNode('VXX', date, 'sell'))
                    hold_vxx = False
                if hold_xiv is False and self.bull_market_p(date):
                        trade_nodes.append(TradeNode('XIV', date, 'buy'))  # short vxx
                        hold_xiv = True
            else:
                if hold_xiv:
                    trade_nodes.append(TradeNode('XIV', date, 'sell'))
                    hold_xiv = False
                if hold_vxx is False and self.bull_market_p(date):
                    trade_nodes.append(TradeNode('VXX', date, 'buy'))
                    hold_vxx = True
        returns = list(TradeSimulation.simulate(trade_nodes, dates[0]))
        if print_trade_node:
            for trade_node in trade_nodes:
                print trade_node
        return returns

    def run1(self, ma_window = 7, print_trade_node=True):
        returns = self.get_returns(self.condition1, ma_window, print_trade_node)
        self.plot(returns)

    def run(self, ma_window = 7):
        returns1 = self.get_returns(self.condition1, ma_window)
        returns2 = self.get_returns(self.condition2, ma_window)
        self.plot2(returns1, returns2, ma_window)

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
        ax.set_yscale('log')
        ax.plot(dates, values1, 'r-', label='ma%s_divide'%ma_window)
        ax.plot(dates, values2, 'b-', label='divide_ma%s'%ma_window)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def plot_vxv_vix(self):
        fig, ax = plt.subplots()
        dates = map(lambda x: x[0], self.vix_records)
        ax.plot(dates, self.vxv_values, 'r-', label='vxv')
        ax.plot(dates, self.vix_values, 'b-', label='vix')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def plot_xiv_vxx(self):
        fig, ax1 = plt.subplots()
        xiv_records = YahooEquityDAO().get_all_equity_price_by_symbol('XIV', from_date_str='2013-12-17')
        vxx_records = YahooEquityDAO().get_all_equity_price_by_symbol('VXX', from_date_str='2013-12-17')
        dates = map(lambda x: x[0], xiv_records)[0:756]
        xiv_values = map(lambda x : x[1], xiv_records)[0:756]
        vxx_values = map(lambda x: x[1], vxx_records)[0:756]
        ax2 = ax1.twinx()
        ax1.plot(dates, xiv_values, 'r-', label='xiv')
        ax2.plot(dates, vxx_values, 'b-', label='vxx')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def plot_vxx(self):
        fig, ax = plt.subplots()
        vxx_records = YahooEquityDAO().get_all_equity_price_by_symbol('VXX', from_date_str='2010-12-17')
        vxx_values = map(lambda x: x[1], vxx_records)
        dates = map(lambda x: x[0], vxx_records)
        ax.plot(dates, vxx_values, 'r-', label='vxx')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()



if __name__ == '__main__':
    RollYield().run1(7)
    # RollYield().run1(5)
    # RollYield().plot_xiv_vxx()
    # RollYield().plot_vxv_vix()
    # RollYield().plot_vxx()
    # print RollYield().get_spy_monthly_indicator()
    # print RollYield().bull_market_p(datetime.date(2011, 8, 1))




