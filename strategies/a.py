from wrapi.container import schedule_function
from wrapi.date_rules import date_rules
from wrapi.time_rules import time_rules


def initialize(context):
    schedule_function(
        func=my_func,
        date_rule=date_rules.everyday(),
        time_rule=time_rules.market_close(minutes=32))


def my_func(context, data):
    print '\n----------output for schedule function in a strategy------------'
    print context.portfolio.portfolio_value
    print data.current('SPY')
    print '\n----------end of schedule function in a strategy------------'


def handle_data(context, data):
    print '\n----------output for handle data in a strategy------------'
    print context.portfolio.portfolio_value
    print data.current('SPY')
    print '----------end of handle data in a strategy------------\n'



