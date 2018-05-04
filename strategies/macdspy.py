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
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=121))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=151))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=181))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=211))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=241))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=271))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=301))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=331))
    schedule_function(func=my_func, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(minutes=361))


def get_max_bar(macd_bar):
    max_bar = 0
    for i in range(len(macd_bar)):
        bar = macd_bar[-i-1]
        if bar < 0:
            break
        elif bar > max_bar:
            max_bar = bar
    return max_bar


def get_min_bar(macd_bar):
    min_bar=0
    for i in range(len(macd_bar)):
        bar = macd_bar[-i-1]
        if bar > 0:
            break
        elif bar < min_bar:
            min_bar = bar
    return min_bar


def my_func(context, data):
    symbol = 'SPY'
    records = data.history(symbol, window=120, frequency='30m')
    macd_list = MACD.get_all_macd(records.values, s=7, l=19, m=26)
    macd_bar = map(lambda x: x[-1], macd_list)
    # from talib import MACD
    # print records.values
    # macd_list = MACD(records.values, fastperiod=7, slowperiod=19, signalperiod=26)
    # print macd_list
    # macd_bar = map(lambda x: x[2], macd_list)

    if macd_bar[-2] < 0 < macd_bar[-1]:
        min_bar = get_min_bar(macd_bar[:-2])
        rate = min_bar * 100/records.values[-1]
        # log.info('rate=%s'%rate)
        if context.hold is False and rate < -0.6:
            log.info('%s buy'%data.specified_date_time)
            order_target_percent(symbol, 1)
            context.hold = True
    else:
        if context.hold:
            if macd_bar[-1] < 0 or macd_bar[-1] < get_max_bar(macd_bar) * 0.618:
                log.info('macd_bar[-1]=%s, max_bar=%s'%(macd_bar[-1] , get_max_bar(macd_bar)))
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



