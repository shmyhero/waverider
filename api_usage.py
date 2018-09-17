from wrapi.quantopian import OrderStyle, get_open_orders, order_target, order_target_percent, cancel_order, set_stop_price
from wrapi.context import Context
from wrapi.data import Data
from wrapi.strategy_runner import StrategyRunner

# this file is used for testing any wrapi, feel free to modify it..

if __name__ == '__main__':
    # print get_open_orders(include_option=True)
    # print get_open_orders()
    # print get_open_orders('SVXY')
    # order_target('SPY', 10, OrderStyle.LimitOrder(260))
    # order_target('QQQ', -12)
    # order_target_percent('QQQ', 0)
    # order_target('QQQ', 31, style=OrderStyle.MarketOrder)
    # order_target('SPY', -6, style=OrderStyle.LimitOrder(258.0))
    # cancel_order(53)
    # set_stop_price('SPY', 250)

    # context = Context()
    # print context.portfolio
    # print context.portfolio.portfolio_value
    # print context.portfolio.positions_value
    # print context.portfolio.capital_used
    # print context.portfolio.positions['VNM'].amount
    # print context.portfolio.positions['QQQ'].amount
    # print context.display_all()
    # print context.portfolio.positions['EFA']
    # print context.portfolio.positions['SPY'].symbol
    # print context.portfolio.positions['SPY'].amount
    # print context.portfolio.positions['QQQ'].amount
    # print context.portfolio.positions['SPY'].last_sale_price
    # print context.portfolio.positions['SPY'].cost_basic
    # context.abc = 1
    # print context.abc
    data = Data()
    # s = data.history('SVXY',  window=1440, frequency='1m')
    # print s
    # print s.first_valid_index().to_pydatetime().second
    # print data.history('SPY', 'close', 1, '1d')
    # print data.history(['SPY', 'VIX'], window=252)
    # print data.current(['SPY', 'VIX'])
    # print data.current(['SPY', 'QQQ'])
    # StrategyRunner.run('caa')
    # n9 = ['LMT', 'MO', 'QQQ', 'DIA', 'EFA', 'EEM', 'HYG', 'IEF', 'BIL']
    # # n9 = ['HYG', 'IEF', 'BIL']
    # df = data.history(n9, 'close', 260, '1d')
    # print df[10:50]
    # print data.history('SPY', 'open', 1)[0]
    # print data.current('SPY')
    # s = data.history('SPY', field='close', window=10)
    # print s
    # print data.history('SPY', "price", 391, "1m")
    # print data.current('QQQ')
    # print s
    # import numpy as np
    # print s.shift(2) / 100 * np.sqrt(21) / np.sqrt(252)
    # print 1.25 * np.sqrt(21) / np.sqrt(252)/100



    # s = data.history('SPY', field='high', window=120)
    # indexes = s.index
    # high_list = s.tolist()
    # low_list = data.history('SPY', field='low', window=120).tolist()
    # # print high_list, low_list
    # from utils.indicator import RSI, SAR
    # sar_list = SAR.get_all_sar(high_list, low_list)
    # for i in range(len(indexes)):
    #     print indexes[i], sar_list[i]
    #
    # close_list = data.history('SPY', window=120).tolist()
    # print RSI.get_rsi(close_list, 2)

    # from utils.indicator import RSI
    # print RSI.get_rsi(price_list)
    # print RSI.get_rsi2(price_list)

    # print data.history('SVXY', window=391, frequency='1m')

    # print data.history(['ADBE', 'AVGO', 'AMZN', 'NFLX', 'GOOG'], window=2000)
    # print data.history('SPY', window = 391, frequency='1m')
    print data.history(['QQQ', 'IWM'], 'price', 10, '1d')




