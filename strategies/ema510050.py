from common.configmgr import ConfigMgr
if ConfigMgr.for_back_test:
    from backtest.quantopian import schedule_function, date_rules, time_rules, log, order_target_percent
else:
    from wrapi.quantopian import schedule_function, date_rules, time_rules, log

from utils.indicator import MACD


def initialize(context):
    context.hold = False
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=1))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=31))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=61))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=91))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=211))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=241))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=271))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=301))


def my_func(context, data):
    symbol = '510050'
    records = data.history(symbol, window=120, frequency='30m')
    ema21 = MACD.get_all_ema(records.values, 21)
    ema8 = MACD.get_all_ema(records.values, 8)
    if ema8[-1] > ema21[-1]:
        if context.hold is False:
            log.info('%s buy'%data.specified_date_time)
            order_target_percent(symbol, 1)
            context.hold = True
    else:
        if context.hold:
            order_target_percent(symbol, 0)
            context.hold = False
            log.info('%s sell' % data.specified_date_time)
    # log.info(data.current('QQQ'))
    # log.info(data.history('QQQ', window=2))
    # log.info(data.history('SVXY', window=390, frequency='1m'))
    # order_target_percent('QQQ', 1)


# def handle_data(context, data):
#     # my_func(context, data)
#     log.info(data.current('QQQ'))
#     # print data.history('SVXY', "price", 1440, "1m")
#     # pass



