from wrapi.order import OrderStyle, get_open_orders, order_target, order_target_percent, cancel_order, set_stop_price
from context import Context

if __name__ == '__main__':
    print get_open_orders()
    #print get_open_orders('UBT')
    # order_target('UBT', 10)
    # order_target('QQQ', 12)
    # order_target_percent('SPY', 0.05)
    # order_target('QQQ', 31, style=OrderStyle.MarketOrder)
    # order_target('SPY', -6, style=OrderStyle.LimitOrder(258.0))
    # cancel_order(100069)
    # set_stop_price('SPY', 250)
    context = Context()
    print context.portfolio.portfolio_value
    print context.portfolio.positions_value
    print context.portfolio.capital_used
    print context.portfolio.positions
    print context.portfolio.positions['SPY'].symbol
    print context.portfolio.positions['SPY'].amount
    print context.portfolio.positions['SPY'].last_sale_price
    print context.portfolio.positions['SPY'].cost_basic


