import pandas as pd
from utils.logger import DailyLoggerFactory
from common.pathmgr import PathMgr
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


class Order(object):

    def __init__(self):
        pass

    @staticmethod
    def get_logger():
        return DailyLoggerFactory.get_logger(__name__, PathMgr.get_log_path())

    @staticmethod
    def order(asset, amount, style=OrderStyle.MarketOrder, sec_type='STK', trade_trace_fn=None):
        # if trade_trace_fn is not None:
        #     trade_trace_fn(asset, amount)
        [order_type, price] = style
        if amount > 0:
            return API().order(asset, sec_type, order_type, amount, 'BUY', price)
        elif amount < 0:
            return API().order(asset, sec_type, order_type, -amount, 'SELL', price)
        else:
            pass
        if trade_trace_fn is not None and amount != 0:
            trade_trace_fn(asset, amount)

    @staticmethod
    def order_target(asset, amount, style=OrderStyle.MarketOrder, sec_type='STK', trade_trace_fn=None):
        portfolio = API().get_portfolio_info()
        delta_amount = amount-portfolio.positions[asset].amount
        return Order.order(asset, delta_amount, style, sec_type, trade_trace_fn)

    @staticmethod
    def order_target_percent(asset, percent, style=OrderStyle.MarketOrder, sec_type='STK', trade_trace_fn=None):
        if percent == 0:
            Order.order_target(asset, 0, style, sec_type, trade_trace_fn)
        else:
            portfolio = API().get_portfolio_info()
            current_percent = portfolio.get_percentage(asset)
            order_cash = (percent - current_percent) * portfolio.net_liquidation
            message_tempalte = """percent=%s, 
                                  current_percent=%s, 
                                  net_liquidation=%s, 
                                  order_cash=%s, 
                                  available_funds=%s"""
            message = message_tempalte % (percent, current_percent, portfolio.net_liquidation, order_cash, portfolio.available_funds)
            Order.get_logger().info(message)
            # if order_cash < portfolio.available_funds:
            try:
                market_price = API().get_market_price(asset)
            except Exception:
                from wrapi.data import Data
                market_price = Data().current(asset)
            amount = int(round(order_cash/market_price))
            return Order.order(asset, amount, style, sec_type, trade_trace_fn)


    @staticmethod
    def get_open_orders(asset=None, include_option=False):
        orders = API().get_open_orders(include_option)
        if asset:
            orders = filter(lambda x: x[1] == asset, orders)
        rows = map(lambda x: x[1:], orders)
        orderids = map(lambda x: int(x[0]), orders)
        fields = ['symbol', 'action', 'quantity']
        return pd.DataFrame(rows, columns=fields, index=orderids)

    @staticmethod
    def cancel_order(order_id):
        API().cancel_order(order_id)

    @staticmethod
    def set_stop_price(asset, stop_price):
        quantity = API().get_portfolio_info().get_quantity(asset)
        return Order.order_target(asset, -quantity, OrderStyle.StopOrder(stop_price))

if __name__ == '__main__':
    # API related functions below:
    print Order.get_open_orders()
    # Order.order_target('SPY', 10)
    #order_target_percent('AAPL', 0.01)
    #order_target('QQQ', 30, style=OrderStyle.MarketOrder)
    #order_target('SPY', 12, style=OrderStyle.StopOrder(249.0))
    #cancel_order(100013)


