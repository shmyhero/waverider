from wrapi.quantopian import schedule_function, date_rules, time_rules, log


def initialize(context):
    schedule_function(
        func=my_func,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_close(minutes=1))


def my_func(context, data):
    # print context.portfolio.positions_value
    # log.info(data.current('QQQ'))
    # log.info(data.history('QQQ', window=2))
    log.info(data.history('SVXY', window=390, frequency='1m'))


# def handle_data(context, data):
#     # my_func(context, data)
#     log.info(data.current('SVXY'))
#     # print data.history('SVXY', "price", 1440, "1m")
#     # pass

