from utils.iohelper import read_file_to_string, write_to_file
from utils.logger import Logger
from utils.shell import Shell
from utils.stringhelper import string_fetch
from common.pathmgr import PathMgr
from utils.listhelper import list_to_hash
from ibapi.portfolio import Portfolio


class API(object):

    ORDER_ID = 101

    def __init__(self):
        self.logger = Logger(__name__, PathMgr.get_log_path())

    def run_cmd(self, cmd_name, args=[]):
        file_path = PathMgr.get_command_file_path(cmd_name)
        lst = map(str, [file_path] + args)
        cmd = 'python \"{}\"'.format('\" \"'.join(lst))
        self.logger.info('run command: %s'%cmd)
        output = Shell.run_cmd(cmd, True)
        self.logger.info('output: %s'%output, False)
        return output

    @staticmethod
    def parse_contract(content):
        symbol = string_fetch(content, '\'m_symbol\': \'', '\'')
        position = int(string_fetch(content, 'position=', ','))
        market_price = float(string_fetch(content, 'marketPrice=', ','))
        return [symbol, [position, market_price]]

    @staticmethod
    def parse_order(content):
        symbol = string_fetch(content, 'm_symbol\': \'', '\'')
        order_id = string_fetch(content, 'orderId=', ',')
        action = string_fetch(content, 'm_action\': \'', '\'')
        quantity = string_fetch(content, 'm_totalQuantity\': ', ',')
        #lmt_price = string_fetch(content, 'm_lmtPrice\': \'', '\'')
        return [symbol, order_id, action, quantity]

    @staticmethod
    def get_order_id():
        order_file_path = PathMgr.get_data_file_path('orderid.txt')
        order_id = int(read_file_to_string(order_file_path))
        write_to_file(order_file_path, str(order_id + 1))
        return order_id

    def get_portfolio_info(self):
        output = self.run_cmd('account')
        total_cash = float(string_fetch(output, 'TotalCashValue, value=', ','))
        net_liquidation = float(string_fetch(output, 'NetLiquidation, value=', ','))
        items = output.split('<updatePortfolio')
        if len(items) > 0:
            contract_dict = list_to_hash(map(API.parse_contract, items[1:]))
        else:
            contract_dict = {}
        return Portfolio(total_cash, net_liquidation, contract_dict)

    def get_open_orders(self):
        output = self.run_cmd('get_open_orders')
        # print output
        items = output.split('<openOrder ')
        if len(items) > 0:
            orders = map(API.parse_order, items[1:])
        else:
            orders = []
        return orders

    def order(self, symbol, sec_type, order_type, quantity, action, price=None):
        arguments = [API.get_order_id(), symbol, sec_type, order_type, quantity, action]
        if price is not None:
            arguments.append(price)
        output = self.run_cmd('order', arguments)
        print output
        return output

    def get_market_price(self, symbol, sec_type = 'STK', exchange = 'SMART', currency = 'USD', strike = 0.0, expiry = '', action = ''):
        output = self.run_cmd('market', [symbol, sec_type, exchange, currency, strike, expiry, action])
        items = output.split('<tickPrice')
        if len(items) > 1:
            prices = map(lambda x : float(string_fetch(x, 'price=', ',')), items[1:])
            return max(prices)
        else:
            raise Exception('Unable to get market price...')

    def cancel_order(self, order_id):
        output = self.run_cmd('cancel_order', [order_id])
        msg = 'OrderId %s that needs to be cancelled is not found' % order_id
        if msg in output:
            self.logger.error(msg)
            raise Exception(msg)
        else:
            self.logger.info('OrderId %s cancelled'%order_id)


class OrderStyle(object):

    def __init__(self):
        pass

    MarketOrder = ['MKT', None]

    @staticmethod
    def StopOrder(stop_price):
        return ['STP', stop_price]

    @staticmethod
    def LimitOrder(lmt_price):
        return ['LMT', lmt_price]


def order_target(asset, amount, style=OrderStyle.MarketOrder, sec_type='STK'):
    [order_type, price] = style
    if amount > 0:
        API().order(asset, sec_type, order_type, amount, 'BUY', price)
    else:
        API().order(asset, sec_type, order_type, -amount, 'SELL', price)


def order_target_percent(asset, percent, style=OrderStyle.MarketOrder, sec_type = 'STK'):
    portfolio = API().get_portfolio_info()
    current_percent = portfolio.get_percentage(asset)
    order_cash = (percent - current_percent) * portfolio.net_liquidation
    if order_cash < portfolio.total_cash:
        market_price = API().get_market_price(asset)
        amount = int(order_cash/market_price)
        if portfolio.get_quantity(asset) + amount > 0:
            order_target(asset, amount, style)
        else:
            raise Exception('The quantity of asset exceed existing quantity in repository...')
    else:
        raise Exception('The cost of asset exceed total cash...')


def get_open_orders(asset=None):
    orders = API().get_open_orders()
    if asset:
        return filter(lambda x:x[0] == asset, orders)
    else:
        return orders


def cancel_order(order_id):
    API().cancel_order(order_id)


if __name__ == '__main__':
    #print API().get_portfolio_info()
    #print API.get_order_id()
    #print API().get_market_price('GOOG')
    #print API().get_market_price('SPY', 'OPT', strike=258, expiry='20171215', action='CALL')

    # API related functions below:
    print get_open_orders()
    #order_target('SPY', 10)
    #order_target_percent('AAPL', 0.01)
    #order_target('QQQ', 30, style=OrderStyle.MarketOrder)
    #order_target('SPY', 12, style=OrderStyle.StopOrder(249.0))
    #cancel_order(100013)

