import pandas as pd
from ibbasic.api import API


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
        return API().order(asset, sec_type, order_type, amount, 'BUY', price)
    else:
        return API().order(asset, sec_type, order_type, -amount, 'SELL', price)


def order_target_percent(asset, percent, style=OrderStyle.MarketOrder, sec_type = 'STK'):
    portfolio = API().get_portfolio_info()
    current_percent = portfolio.get_percentage(asset)
    order_cash = (percent - current_percent) * portfolio.net_liquidation
    if order_cash < portfolio.total_cash:
        market_price = API().get_market_price(asset)
        amount = int(round(order_cash/market_price))
        return order_target(asset, amount, style)
    else:
        raise Exception('The cost of asset exceed total cash...')


def get_open_orders(asset=None):
    orders = API().get_open_orders()
    if asset:
        orders = filter(lambda x: x[1] == asset, orders)
    rows = map(lambda x: x[1:], orders)
    orderids = map(lambda x: int(x[0]), orders)
    fields = ['symbol', 'action', 'quantity']
    return pd.DataFrame(rows, columns=fields, index=orderids)


def cancel_order(order_id):
    API().cancel_order(order_id)


def set_stop_price(asset, stop_price):
    quantity = API().get_portfolio_info().get_quantity(asset)
    return order_target(asset, -quantity, OrderStyle.StopOrder(stop_price))

if __name__ == '__main__':
    # API related functions below:
    print get_open_orders()
    #order_target('SPY', 10)
    #order_target_percent('AAPL', 0.01)
    #order_target('QQQ', 30, style=OrderStyle.MarketOrder)
    #order_target('SPY', 12, style=OrderStyle.StopOrder(249.0))
    #cancel_order(100013)


