from wrapi.quantopian import schedule_function, date_rules, time_rules, log, order_target, order_target_percent


def initialize(context):
    schedule_function(
        func=my_func,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_open(minutes=69))


def my_func(context, data):
    print '\n----------output for schedule function in a strategy------------'
    print context.portfolio.portfolio_value
    print data.current('SPY')
    print '\n----------end of schedule function in a strategy------------'


def handle_data(context, data):
    log.info('----------output for handle data in a strategy------------')
    # order_target('SPY', 1)
    # order_target_percent('SPY', 0.2)
    # print context.portfolio.portfolio_value
    print data.current('SPY')
    print context.get('spy', 'crash')
    context.set('spy', 'crash', True)
    context.set('spy', 'stop_order_price', 250)
    print context.get('spy', 'crash')
    print context.get('spy', 'stop_order_price')
    # context.end()
    log.info('----------end of handle data in a strategy------------')


