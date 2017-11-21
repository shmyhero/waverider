from wrapi.order import OrderStyle, get_open_orders, order_target, order_target_percent, cancel_order, set_stop_price

if __name__ == '__main__':
    print get_open_orders()
    # print get_open_orders('QQQ')
    # order_target('UBT', 10)
    # order_target_percent('QQQ', 0.0)
    # order_target('QQQ', 31, style=OrderStyle.MarketOrder)
    # order_target('SPY', -6, style=OrderStyle.LimitOrder(258.0))
    # cancel_order(100069)
    # set_stop_price('SPY', 250)
