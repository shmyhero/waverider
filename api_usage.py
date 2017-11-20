from ibapi.api import OrderStyle, get_open_orders, order_target, order_target_percent, cancel_order

if __name__ == '__main__':
    print get_open_orders()
    # print get_open_orders('QQQ')
    # order_target('SPY', 11)
    # order_target_percent('AAPL', 0.01)
    # order_target('QQQ', 31, style=OrderStyle.MarketOrder)
    # order_target('SPY', 13, style=OrderStyle.StopOrder(249.0))
    # cancel_order(100009)
