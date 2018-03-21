import datetime
import pytz
from utils.timezonehelper import get_delta_hour_to_us_east
from utils.iohelper import read_file_to_string, write_to_file
from utils.logger import Logger
from utils.shell import Shell
from utils.stringhelper import string_fetch
from utils.mathhelper import average
from common.pathmgr import PathMgr
from utils.listhelper import list_to_hash
from ibbasic.portfolio import Portfolio


class API(object):

    def __init__(self):
        self.logger = Logger(__name__, PathMgr.get_log_path())

    def run_cmd(self, cmd_name, args=[]):
        file_path = PathMgr.get_command_file_path(cmd_name)
        lst = map(str, [file_path] + args)
        cmd = 'python \"{}\"'.format('\" \"'.join(lst))
        self.logger.info('run command: %s'%cmd)
        output = Shell.run_cmd(cmd, True)
        if 'errorCode=502' in output:
            raise Exception(output)
        self.logger.info('output: %s'%output, False)
        return output

    @staticmethod
    def parse_contract(content):
        symbol = string_fetch(content, 'm_localSymbol\': \'', '\'')
        symbol = symbol.replace(' ', '')
        quantity = int(string_fetch(content, 'position=', ','))
        market_price = float(string_fetch(content, 'marketPrice=', ','))
        cost_price = float(string_fetch(content, 'averageCost=', ','))
        return [symbol, [quantity, market_price, cost_price]]

    @staticmethod
    def parse_order(content):
        symbol = string_fetch(content, 'm_localSymbol\': \'', '\'')
        symbol = symbol.replace(' ', '')
        order_id = string_fetch(content, 'orderId=', ',')
        action = string_fetch(content, 'm_action\': \'', '\'')
        quantity = string_fetch(content, 'm_totalQuantity\': ', ',')
        # lmt_price = string_fetch(content, 'm_lmtPrice\': \'', '\'')
        return [order_id, symbol, action, quantity]

    @staticmethod
    def get_order_id():
        order_file_path = PathMgr.get_data_file_path('orderid.txt')
        order_id = int(read_file_to_string(order_file_path))
        write_to_file(order_file_path, str(order_id + 1))
        return order_id

    @staticmethod
    def validate_order_output(output):
        server_error_msg = 'Server Error:'
        if server_error_msg in output:
            items = output.split(server_error_msg)[1:]
            error_items = map(lambda x: [string_fetch(x, 'errorCode=', ','), string_fetch(x, 'errorMsg=', '>')], items)
            ignore_error_codes = ['2104', '2106', '2107', '399']  # 399 for market not open
            filtered_error_items = filter(lambda x: x[0] not in ignore_error_codes, error_items)
            if len(filtered_error_items) > 0:
                exception_msg = str(map(lambda x: 'errorCode={}, errorMsg={}'.format(x[0], x[1]), filtered_error_items))
                raise Exception(exception_msg)

    def get_portfolio_info(self):
        output = self.run_cmd('account')
        if output == '':
            raise Exception('Failed to get account info, please check the IB gateway, config, network and ibpy2 packages, etc...')
        str_available_funds = string_fetch(output, 'AvailableFunds, value=', ',')
        # self.logger.info("available_funds string value: %s"%str_available_funds)
        available_funds = float(str_available_funds)
        str_net_liquidation = string_fetch(output, 'NetLiquidation, value=', ',')
        # self.logger.info("net_liquidation string value: %s" % str_net_liquidation)
        net_liquidation = float(str_net_liquidation)
        items = output.split('<updatePortfolio')
        if len(items) > 0:
            contract_dict = list_to_hash(map(API.parse_contract, items[1:]))
        else:
            contract_dict = {}
        return Portfolio(available_funds, net_liquidation, contract_dict)

    def get_open_orders(self):
        output = self.run_cmd('get_open_orders')
        # print output
        items = output.split('<openOrder ')
        if len(items) > 0:
            orders = map(API.parse_order, items[1:])
            orders = filter(lambda x: len(x[1]) < 15, orders)
        else:
            orders = []
        return orders

    def order(self, symbol, sec_type, order_type, quantity, action, price=None):
        order_id = API.get_order_id()
        arguments = [order_id, symbol, sec_type, order_type, quantity, action]
        if price is not None:
            arguments.append(price)
        output = self.run_cmd('order', arguments)
        API.validate_order_output(output)
        return order_id

    def get_market_price(self, symbol, sec_type = 'STK', exchange = 'SMART', currency = 'USD', strike = 0.0, expiry = '', action = ''):
        output = self.run_cmd('market', [symbol, sec_type, exchange, currency, strike, expiry, action])
        if 'errorCode=2119' in output:
            output = self.run_cmd('market', [symbol, sec_type, exchange, currency, strike, expiry, action])
        items = output.split('<tickPrice')
        if len(items) > 1:
            prices = map(lambda x: float(string_fetch(x, 'price=', ',')), items[1:])
            prices.sort()
            middle_index = len(prices)/2
            return prices[middle_index]
        else:
            raise Exception('Unable to get market price from IB...')

    def parse_historical_data(self, line, delta_hour=None):
        time_str = string_fetch(line, 'date=', ',')
        if delta_hour is not None:  # min data
            trade_time = datetime.datetime.strptime(time_str, '%Y%m%d %H:%M:%S')-delta_hour
        else:  # daily data
            trade_time = datetime.datetime.strptime(time_str, '%Y%m%d').date()
        open = float(string_fetch(line, 'open=', ','))
        high = float(string_fetch(line, 'high=', ','))
        low = float(string_fetch(line, 'low=', ','))
        close = float(string_fetch(line, 'close=', ','))
        return [trade_time, open, high, low, close]

    def get_historical_data(self, symbol, days, barsize):
        output = self.run_cmd('history', [symbol, days, barsize])
        if 'errorCode=162' in output:
            output = self.run_cmd('history', [symbol, days, barsize])
        items = output.split('<historicalData')
        if len(items) > 1:
            # print len(items)-2
            if barsize == 'min':
                delta_hour = get_delta_hour_to_us_east()
                return map(lambda x: self.parse_historical_data(x, delta_hour), items[1:-1])
            else:
                return map(self.parse_historical_data, items[1:-1])
        else:
            raise Exception('Unable to get historical price from IB...')

    def cancel_order(self, order_id):
        output = self.run_cmd('cancel_order', [order_id])
        msg = 'OrderId %s that needs to be cancelled is not found' % order_id
        if msg in output:
            self.logger.error(msg)
            raise Exception(msg)
        else:
            self.logger.info('OrderId %s cancelled'%order_id)

if __name__ == '__main__':
    # print API().get_portfolio_info()
    # print API.get_order_id()
    # print API().get_market_price('GOOG')
    #print API().get_market_price('SPY', 'OPT', strike=258, expiry='20171215', action='CALL')
    print API().get_historical_data('SPY', '20', 'day')
    # print API().get_historical_data('SPY', '5', 'min')


