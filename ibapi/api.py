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
    def get_order_id():
        order_file_path = PathMgr.get_data_file_path('orderid.txt')
        order_id = int(read_file_to_string(order_file_path))
        write_to_file(order_file_path, str(order_id%65536+1))
        return order_id

    def get_portfolio_info(self):
        output = self.run_cmd('account')
        total_cash = float(string_fetch(output, 'TotalCashValue, value=', ','))
        net_liquidation = float(string_fetch(output, 'NetLiquidation, value=', ','))
        items = output.split('<updatePortfolio')
        if len(items) > 0:
            contract_dict =  list_to_hash(map(API.parse_contract, items[1:]))
        else:
            contract_dict = {}
        return Portfolio(total_cash, net_liquidation, contract_dict)

    def order(self, symbol, sec_type, order_type, quantity, action):
        output = self.run_cmd('order', [API.get_order_id(), symbol, sec_type, order_type, quantity, action])
        return output

    def get_market_price(self, symbol, sec_type = 'STK', exchange = 'SMART', currency = 'USD', strike = 0.0, expiry = '', action = ''):
        output = self.run_cmd('market', [symbol, sec_type, exchange, currency, strike, expiry, action])
        items = output.split('<tickPrice')
        if len(items) > 1:
            prices = map(lambda x : float(string_fetch(x, 'price=', ',')), items[1:])
            return max(prices)
        else:
            return None

    # obsoleted
    def get_symbol_quantity(self, symbol):
        h = self.get_contract_info()
        if h.has_key(symbol):
            return h[symbol][0]
        else:
            return 0


def order_target(asset, amount, style='MKT', sec_type='STK'):
    if amount > 0:
        API().order(asset, sec_type, style, amount, 'BUY')
    else:
        API().order(asset, sec_type, style, -amount, 'SELL')


def order_target_percent(asset, percent, style='MKT', sec_type = 'STK'):
    portfolio = API().get_portfolio_info()
    current_percent = portfolio.get_percentage(asset)
    order_cash = (percent - current_percent) * portfolio.net_liquidation
    if order_cash < portfolio.total_cash:
        market_price = API().get_market_price(asset)
        amount = int(order_cash/market_price)
        if portfolio.get_quantity(asset) + amount > 0:
            order_target(asset, amount)
        else:
            raise Exception('The quantity of asset exceed existing quantity in repository...')
    else:
        raise Exception('The cost of asset exceed total cash...')


if __name__ == '__main__':
    #print API().get_portfolio_info()
    #print API.get_order_id()
    #print API().get_market_price('SPY')
    #print API().get_market_price('SPY', 'OPT', strike=255.0, expiry='20171215', action='CALL')
    #order_target('SPY', 10)
    order_target_percent('QQQ', 0.1)

