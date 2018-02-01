import datetime
import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataaccess.db import YahooEquityDAO
from research.tradesimulation import TradeNode, TradeSimulation


class VIXBasic(object):

    def __init__(self):
        self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str='2006-07-17')
        self.vxv_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VXV', from_date_str='2006-07-17')
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

    def plot_2symbol(self, symbol1, symbol2):
        fig, ax = plt.subplots()
        records1 = YahooEquityDAO().get_all_equity_price_by_symbol(symbol1, from_date_str='2006-07-17')
        records2 = YahooEquityDAO().get_all_equity_price_by_symbol(symbol2, from_date_str='2006-07-17')
        values1 = map(lambda x: x[1], records1)
        values2 = map(lambda x: x[1], records2)
        dates = map(lambda x: x[0], records1)
        ax.plot(dates, values1, 'r-', label=symbol1)
        ax.plot(dates, values2, 'b-', label=symbol2)
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
        xiv_records = YahooEquityDAO().get_all_equity_price_by_symbol('XIV', from_date_str='2006-07-17')
        vxx_records = YahooEquityDAO().get_all_equity_price_by_symbol('VXX', from_date_str='2006-07-17')
        dates = map(lambda x: x[0], xiv_records)
        xiv_values = map(lambda x : x[1], xiv_records)
        vxx_values = map(lambda x: x[1], vxx_records)
        ax2 = ax1.twinx()
        ax1.plot(dates, xiv_values, 'r-', label='xiv')
        ax2.plot(dates, vxx_values, 'b-', label='vxx')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def plot_symbol(self, symbol):
        fig, ax = plt.subplots()
        records = YahooEquityDAO().get_all_equity_price_by_symbol(symbol, from_date_str='2006-07-17')
        values = map(lambda x: x[1], records)
        dates = map(lambda x: x[0], records)
        ax.plot(dates, values, 'r-', label=symbol)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def plot_symbol_with_ma(self, symbol, ma_window):
        fig, ax = plt.subplots()
        records = YahooEquityDAO().get_all_equity_price_by_symbol(symbol, from_date_str='2006-07-17')
        values = map(lambda x: x[1], records)
        dates = map(lambda x: x[0], records)[ma_window:]
        values1 = pd.Series(values).rolling(window=5).mean().tolist()[5:]
        ma_values = pd.Series(values).rolling(window=ma_window).mean().tolist()[ma_window:]
        ax.plot(dates, values1[15:], 'r-', label=symbol)
        ax.plot(dates, ma_values, 'b-', label='%s_ma%s'% (symbol, ma_window))
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

    def plot_z_score(self, ma_window_short=7, ma_window_long=20):
        rate = map(lambda x, y: x / y, self.vxv_values, self.vix_values)
        rate_ma_short = pd.Series(rate).rolling(window=ma_window_short).mean().tolist()
        rate_ma_long = pd.Series(rate).rolling(window=ma_window_long).mean().tolist()
        rate_std = pd.Series(rate).rolling(window=ma_window_long).std().tolist()
        zscore = map(lambda x, y, z: (x - y) / z, rate_ma_short[ma_window_long:], rate_ma_long[ma_window_long:],
                     rate_std[ma_window_long:])
        dates = map(lambda x: x[0], self.vxv_records)[ma_window_long:]
        fig, ax = plt.subplots()
        ax.plot(dates, zscore, label='zscore')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
        plt.show()

if __name__ == '__main__':
    # VIXBasic().plot_xiv_vxx()
    # VIXBasic().plot_2symbol('vxv', 'vix')
    # VIXBasic().plot_2symbol('vxmt', 'vxv')
    # VIXBasic().p
    # lot_symbol('VXX')
    # VIXBasic().plot_symbol('^VIX')
    # VIXBasic().plot_symbol('SPY')
    # VIXBasic().plot_symbol('XIV')
    # VIXBasic().plot_symbol('VXX')
    # VIXBasic().plot_symbol_with_ma('SPY', 20)
    VIXBasic().plot_z_score()




