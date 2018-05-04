from common.configmgr import ConfigMgr
if ConfigMgr.for_back_test:
    from backtest.quantopian import schedule_function, date_rules, time_rules, log, get_open_orders, is_market_open, order_target_percent
else:
    from wrapi.quantopian import schedule_function, date_rules, time_rules, log, get_open_orders, is_market_open, order_target_percent


def initialize(context):
    schedule_function(
        func=my_func,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_close(minutes=1))


def my_func(context, data):
    # print context.portfolio.positions_value
    # log.info(data.current('QQQ'))
    log.info(data.history('QQQ', window=2))
    # log.info(data.history('SVXY', window=390, frequency='1m'))


def handle_data(context, data):
    order_target_percent('AGG', 1)

def order_target_ratio(context, data, stock, ratio):
    if not is_market_open():
        log.warning( 'Market is not opened, order canceled : ' + stock + ' : ' + str(ratio))
        return
    if len(get_open_orders(stock)) != 0:
        log.warning( 'There are remained orders for stock : ' + stock + ', order canceled.')
        return
    order_target_percent(stock, ratio)
    log.info('%s ratio : %s ' % (stock, str(round(ratio, 2))))



