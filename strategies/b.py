from wrapi.container import schedule_function
from wrapi.date_rules import date_rules
from wrapi.time_rules import time_rules


def initialize(context):
    schedule_function(
        func=my_func,
        date_rule=date_rules.everyday(),
        time_rule=time_rules.market_close(minutes=1))


def my_func(context, data):
    print context.portfolio.positions_value
    print data.current('QQQ')


#def handle_data(context, data):
#    print '\n----------output for handle data in b strategy------------'
#    print context.portfolio.positions_value
#    print data.current('QQQ')
#    print '----------end of handle data in b strategy------------\n'


