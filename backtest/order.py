import pandas as pd


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

    def __init__(self, api):
        self.api = api

    def order(self, asset, amount, style=OrderStyle.MarketOrder, sec_type='STK', trade_trace_fn=None):
        self.api.order(asset, amount)
        if trade_trace_fn is not None and amount != 0:
            trade_trace_fn(asset, amount)

    def order_target(self, asset, amount, style=OrderStyle.MarketOrder, sec_type='STK', trade_trace_fn=None):
        portfolio = self.api.get_portfolio_info()
        delta_amount = amount-portfolio.positions[asset].amount
        return self.order(asset, delta_amount, style, sec_type, trade_trace_fn)

    def order_target_percent(self, asset, percent, style=OrderStyle.MarketOrder, sec_type='STK', trade_trace_fn=None):
        if percent == 0:
            self.order_target(asset, 0, style, sec_type, trade_trace_fn)
        else:
            portfolio = self.api.get_portfolio_info()
            current_percent = portfolio.get_percentage(asset, self.api.data)
            order_cash = (percent - current_percent) * portfolio.get_portfolio_value(self.api.data)
            # if order_cash < portfolio.available_funds:
            market_price = self.api.data.get_market_price(asset)
            amount = int(round(order_cash/market_price))
            return self.order(asset, amount, style, sec_type, trade_trace_fn)
            # else:
            #     raise Exception('The cost of asset exceed total cash...')

    def get_open_orders(self, asset=None, include_option=False):
        rows = []
        fields = ['symbol', 'action', 'quantity']
        return pd.DataFrame(rows, columns=fields)

    def cancel_order(self, order_id):
        pass

    def set_stop_price(self, asset, stop_price):
        # quantity = API().get_portfolio_info().get_quantity(asset)
        # return Order.order_target(asset, -quantity, OrderStyle.StopOrder(stop_price))
        pass

if __name__ == '__main__':
    # API related functions below:
    print Order.get_open_orders()
    # Order.order_target('SPY', 10)
    #order_target_percent('AAPL', 0.01)
    #order_target('QQQ', 30, style=OrderStyle.MarketOrder)
    #order_target('SPY', 12, style=OrderStyle.StopOrder(249.0))
    #cancel_order(100013)


