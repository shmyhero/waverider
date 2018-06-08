from common.configmgr import ConfigMgr
if ConfigMgr.for_back_test:
    from backtest.quantopian import schedule_function, date_rules, time_rules, log, order_target_percent, symbol
else:
    from wrapi.quantopian import schedule_function, date_rules, time_rules, log

from utils.indicator import MACD


def initialize(context):
    context.set_slippage(0.0002)
    context.hold_long = False
    context.hold_short = False
    context.equity = symbol('SPY')
    context.long_equity = symbol('SPY')
    context.x = 26
    context.macd_list = []
    context.macd_setting = [7, 19, 26]
    context.golden_ratio = 0.618
    for i in range(390 / context.x - 1):
        schedule_function(func=my_func, date_rule=date_rules.every_day(),
                          time_rule=time_rules.market_open(minutes=(i + 1) * context.x))


def get_max_bar(context):
    max_bar = 0
    for i in range(len(context.macd_list)):
        bar = context.macd_list[-i-1][-1]
        if bar < 0:
            break
        elif bar > max_bar:
            max_bar = bar
    return max_bar

def get_min_bar(context):
    min_bar=0
    for i in range(len(context.macd_list)):
        bar = context.macd_list[-i-1][-1]
        if bar > 0:
            break
        elif bar < min_bar:
            min_bar = bar
    return min_bar


def my_func(context, data):
    current_price = data.current(context.equity)
    append_macd(context, current_price)
    handle_macd(context, data)


def append_macd(context, price):
    [s, l, m] = context.macd_setting
    [ema_short, ema_long, dif, dea, bar] = [None, None, None, None, None]
    if len(context.macd_list) > 0:
        [ema_short, ema_long, dif, dea, bar] = context.macd_list[-1]
    new_macd = MACD.get_new_macd(ema_short, ema_long, dea, price, s, l, m)
    context.macd_list.append(new_macd)


def handle_macd(context, data):
    if len(context.macd_list) < context.x:
        return
    long_strategy(context, data)


def long_action(context, data):
    clear_short_action(context, data)
    if context.hold_long is False:
        order_target_percent(context.long_equity, 1)
        # record_buy(context, data.current(context.long_equity, 'price'))
        context.hold_long = True


def short_action(context, data):
    clear_long_action(context, data)
    if context.hold_short is False:
        order_target_percent(context.short_equity, 1)
        # record_buy(context, data.current(context.short_equity, 'price'))
        context.hold_short = True


def clear_long_action(context, data):
    if context.hold_long:
        order_target_percent(context.long_equity, 0)
        # record_sell(context, data.current(context.long_equity, 'price'))
        context.hold_long = False


def clear_short_action(context, data):
    if context.hold_short:
        order_target_percent(context.short_equity, 0)
        # record_sell(context, data.current(context.short_equity, 'price'))
        context.hold_short = False


def long_strategy(context, data):
    macd_bar = map(lambda x: x[-1], context.macd_list[-3:])
    if macd_bar[-2] < 0 <= macd_bar[-1]:
        long_action(context, data)
    elif macd_bar[-1] < 0:
        min_bar = get_min_bar(context)
        negative_threshold = min_bar * 0.236  # context.golden_ratio*0.382
        if macd_bar[-1] > negative_threshold:
            long_action(context, data)
        elif macd_bar[-1] < negative_threshold:
            clear_long_action(context, data)
    else:
        threshold = get_max_bar(context) * context.golden_ratio
        if (macd_bar[-1] < 0 or macd_bar[-1] <= threshold) and macd_bar[-2] > 0:
            clear_long_action(context, data)
        else:
            if macd_bar[-1] > threshold:
                long_action(context, data)


