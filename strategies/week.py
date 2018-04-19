from common.configmgr import ConfigMgr
if ConfigMgr.for_back_test:
    from backtest.quantopian import schedule_function, date_rules, time_rules, log, order_target_percent, symbol
else:
    from wrapi.quantopian import schedule_function, date_rules, time_rules, log, symbol


def initialize(context):
    schedule_function(short_oil, date_rules.week_start(), time_rules.market_open())
    schedule_function(cover_oil, date_rules.week_start(1), time_rules.market_open())
    schedule_function(long_spy, date_rules.week_start(1), time_rules.market_open())
    schedule_function(close_out_spy, date_rules.week_start(2), time_rules.market_open())
    schedule_function(long_gld, date_rules.week_start(4), time_rules.market_open())
    schedule_function(close_out_gld, date_rules.week_start(0), time_rules.market_open())


def short_oil(context, data):
    order_target_percent(symbol('OIL'), -0.5)


def cover_oil(context, data):
    order_target_percent(symbol('OIL'), 0)


def long_spy(context, data):
    open_price = data.history(symbol('SPY'), 'open', 1, '1d')[0]
    close_price = data.history(symbol('SPY'), 'close', 1, '1d')[0]
    if close_price < open_price:
        order_target_percent(symbol('SPY'), 0.5)


def close_out_spy(context, data):
    order_target_percent(symbol('SPY'), 0)


def long_gld(context, data):
    order_target_percent(symbol('GLD'), 1)


def close_out_gld(context, data):
    order_target_percent(symbol('GLD'), 0)




