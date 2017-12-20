from wrapi.quantopian import schedule_function, date_rules, time_rules, log


def initialize(context):
    schedule_function(
        func=my_func,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_close(minutes=1))


def my_func(context, data):
    print context.portfolio.positions_value
    log.info(data.current('QQQ'))


def handle_data(context, data):
    my_func(context, data)

