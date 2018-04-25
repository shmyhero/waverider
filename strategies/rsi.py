from common.configmgr import ConfigMgr
if ConfigMgr.for_back_test:
    from backtest.quantopian import schedule_function, date_rules, time_rules, log, order_target_percent, symbol
else:
    from wrapi.quantopian import schedule_function, date_rules, time_rules, log, symbol
import talib


def initialize(context):
    context.hold = False


def handle_data(context, data):
    """
    Called every minute.
    """
    asset = symbol('SVXY')
    series = data.history(asset, 'price', 30, '1m')
    # print series.values
    rsi = talib.RSI(series.values, timeperiod=12)
    # print rsi6
    # print series
    # print series[-1], series[0]
    if rsi[-1] < 20:
        # order_target_percent(asset, 1.0)
        if context.hold is False:
            order_target_percent(asset, 1.0)
            context.hold = True
            print 'Buy: %s' % data.history(asset, 'price', 1, '1m')
    elif rsi[-1] > 80:
        # order_target_percent(asset, 0)
        if context.hold:
            order_target_percent(asset, 0)
            context.hold = False
            log.info('Sell: %s' % data.history(asset, 'price', 1, '1m'))
    else:
        pass