from wrapi.container import schedule_function
from wrapi.date_rules import date_rules
from wrapi.time_rules import time_rules
from wrapi.qutopian_functions import log


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
    print context.portfolio.portfolio_value
    print data.current('SPY')
    log.info('----------end of handle data in a strategy------------')



