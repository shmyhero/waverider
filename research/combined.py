import datetime
import pandas as pd
import matplotlib.pyplot as plt
from utils.optioncalculator import OptionCalculator
from dataaccess.db import YahooEquityDAO
from research.tradesimulation import TradeNode, TradeSimulation


class RollYield(object):

    def __init__(self):
        self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str='2010-12-17')
        self.vxv_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VXV', from_date_str='2010-12-17')
        self.vix_values = map(lambda x: x[1], self.vix_records)
        self.vxv_values = map(lambda x: x[1], self.vxv_records)

    def condition(self, ma_window):
        vxv_ma = pd.Series(self.vxv_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        vix_ma = pd.Series(self.vix_values).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x, y: x > y, vxv_ma, vix_ma)

    def get_returns(self, ma_window=7, print_trade_node=False):
        trade_nodes = []
        previous_condition = False
        conditions = self.condition(ma_window)
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
        if print_trade_node:
            for trade_node in trade_nodes:
                print trade_node
        return returns


class VRP(object):

    """Volatility risk premium """
    def __init__(self, vol_circle=10):
        from_date_str = '2010-12-02'
        spy_records = YahooEquityDAO().get_all_equity_price_by_symbol('SPY', from_date_str)
        self.vol_list = OptionCalculator.get_year_history_volatility_list(spy_records, vol_circle)
        self.vix_records = YahooEquityDAO().get_all_equity_price_by_symbol('^VIX', from_date_str)[vol_circle:]
        self.vol_values = map(lambda x: x[1]*100, self.vol_list)
        self.vix_values = map(lambda x: x[1], self.vix_records)

    def condition(self, ma_window):
        delta_list = map(lambda x, y: x-y, self.vix_values, self.vol_values)
        ma_delta_list = pd.Series(delta_list).rolling(window=ma_window).mean().tolist()[ma_window:]
        return map(lambda x: x > 0, ma_delta_list)

    def get_returns(self, ma_window=8):
        trade_nodes = []
        previous_condition = False
        conditions = self.condition(ma_window)
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
        # for trade_node in trade_nodes:
        #    print trade_node
        return returns


def plot2():
    returns1 = RollYield().get_returns()
    returns2 = VRP().get_returns()
    dates = map(lambda x: x[0], returns1)
    values1 = map(lambda x: x[1], returns1)
    values2 = map(lambda x: x[1], returns2)
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.plot(dates, values1, 'r-', label='roll yield')
    ax.plot(dates, values2, 'b-', label='VRP')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=8, borderaxespad=0.)
    plt.show()


if __name__ == '__main__':
    plot2()

