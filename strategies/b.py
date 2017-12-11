from wrapi.container import schedule_function
from wrapi.date_rules import date_rules
from wrapi.time_rules import time_rules
from wrapi.qutopian_functions import log


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

