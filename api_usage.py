from wrapi.order import OrderStyle, get_open_orders, order_target, order_target_percent, cancel_order, set_stop_price
from wrapi.context import Context
from wrapi.data import Data
from wrapi.strategy_runner import StrategyRunner

if __name__ == '__main__':
    # print get_open_orders()
    # print get_open_orders('UBT')
    # order_target('SPY', 10, OrderStyle.LimitOrder(260))
    # order_target('QQQ', -12)
    # order_target_percent('SPY', 0)
    # order_target('QQQ', 31, style=OrderStyle.MarketOrder)
    # order_target('SPY', -6, style=OrderStyle.LimitOrder(258.0))
    # cancel_order(100135)
    # set_stop_price('SPY', 250)
    # context = Context()
    # print context.portfolio.portfolio_value
    # print context.portfolio.positions_value
    # print context.portfolio.capital_used
    # print context.portfolio.positions
    # print context.portfolio.positions['SPY'].symbol
    # print context.portfolio.positions['SPY'].amount
    # print context.portfolio.positions['QQQ'].amount
    # print context.portfolio.positions['SPY'].last_sale_price
    # print context.portfolio.positions['SPY'].cost_basic
    # context.abc = 1
    # print context.abc
    # data = Data()
    # print data.history('QQQ', field='close', window=100)
    # print data.history(['SPY', 'VIX'], window=252)
    # print data.current(['SPY', 'VIX'])
    StrategyRunner.run('caa')



