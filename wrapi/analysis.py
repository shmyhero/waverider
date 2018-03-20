import datetime
import pytz
import os
import json
import math
import numpy as np
from utils.iohelper import read_file_to_string, append_to_file, write_to_file, ensure_parent_dir_exists
from common.pathmgr import PathMgr
from wrapi.order import OrderStyle
from wrapi.data import Data
from ibbasic.api import API
from ibbasic.portfolio import Portfolio


class TradeRecord(object):

    @staticmethod
    def read_from_line(line):
        record = line.split(',')
        time = datetime.datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
        symbol = record[1]
        amount = int(record[2])
        price = float(record[3])
        return TradeRecord(time, symbol, amount, price)

    def __init__(self, time, symbol, amount, price):
        self.time = time
        self.symbol = symbol
        self.amount = amount
        self.price = price

    def __str__(self):
        return str(self.__dict__)


class TradeRecordDAO(object):

    @staticmethod
    def write_trade_trace(strategy_name, asset, amount, style):
        file_path = PathMgr.get_strategies_tradetrace_file(strategy_name)
        time = datetime.datetime.now(tz=pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
        if style == OrderStyle.MarketOrder:
            price = Data().current(asset)
        else:
            price = style[1]
        content = ','.join(map(str, [time, asset, amount, price]))
        append_to_file(file_path, '%s\r\n' % content)

    @staticmethod
    def read_trade_trace(strategy_name):
        file_path = PathMgr.get_strategies_tradetrace_file(strategy_name)
        content = read_file_to_string(file_path)
        lines = content.split('\r\n')[:-1]
        return map(TradeRecord.read_from_line, lines)


class PortfolioDAO(object):

    @staticmethod
    def save_portfolio_info(strategy_name):
        date = datetime.datetime.now(tz=pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
        dic = PortfolioDAO.read_porfolio_info(strategy_name)
        dic[date] = API().get_portfolio_info().to_dict()
        file_path = PathMgr.get_strategies_portfolio_file(strategy_name)
        ensure_parent_dir_exists(file_path)

        write_to_file(file_path, json.dumps(dic))

    @staticmethod
    def read_porfolio_info(strategy_name):
        file_path = PathMgr.get_strategies_portfolio_file(strategy_name)
        if os.path.exists(file_path):
            content = read_file_to_string(file_path)
            dic = json.loads(content)
            # for key in dic.keys():
                # dic[key] = Portfolio.from_dict(dic[key])
            return dic
        else:
            return {}


class Analysis(object):

    def __init__(self, strategy_name):
        self.strategy_name = strategy_name
        self.trade_trace = TradeRecordDAO.read_trade_trace(strategy_name)
        self.portfolio_info = PortfolioDAO.read_porfolio_info(strategy_name)
        self.net_liquidations = self.get_netliquidations()
        self.returns = self.get_returns()
        spy_values = Data().history('SPY', window=len(self.net_liquidations)).values
        self.bench_mark_returns = self.get_returns(spy_values)

    def get_netliquidations(self):
        records = []
        for k, v in self.portfolio_info.iteritems():
            date = datetime.datetime.strptime(k, '%Y-%m-%d')
            value = v['net_liquidation']
            records.append([date, value])
        records.sort(key=lambda x: x[0])
        return records

    def get_returns(self, values=None):
        if values is None:
            values = map(lambda x: x[1], self.net_liquidations)
        base = values[0]
        return map(lambda x: x/base, values)

    def get_start_date(self):
        return self.net_liquidations[0][0]

    def get_end_date(self):
        return self.net_liquidations[-1][0]

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
    # print PortfolioDAO.read_portfolio_info('a')
    # PortfolioDAO.save_portfolio_info('a')
    analysis = Analysis('a')
    print analysis.get_cumulative_return()
    print analysis.get_annual_return()
    print analysis.get_max_draw_down()
    print analysis.get_annual_volatility()
    print analysis.get_sharpe_ratio()
    beta = analysis.get_beta()
    print beta
    alpha = analysis.get_alpha(beta)
    print alpha

