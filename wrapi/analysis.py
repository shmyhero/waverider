import datetime
import pytz
import os
import json
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
            for key in dic.keys():
                dic[key] = Portfolio.from_dict(dic[key])
            return dic
        else:
            return {}


class Analysis(object):

    def __init__(self, strategy_name):
        self.strategy_name = strategy_name
        self.trade_trace = TradeRecordDAO.read_trade_trace(strategy_name)


if __name__ == '__main__':
    # for trade_record in read_trade_trace('a'):
    #     print trade_record
    # pass
    PortfolioDAO.save_portfolio_info('a')

