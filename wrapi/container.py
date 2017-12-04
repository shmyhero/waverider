from wrapi.context import Context
from wrapi.data import Data

class ScheduleFunction(object):

    def __init__(self, my_func, date_rule, time_rule):
        self.my_func = my_func
        self.date_rule = date_rule
        self.time_rule = time_rule

    def run(self, current_time):
        if self.date_rule.validate(current_time) and self.time_rule.validate(current_time):
            self.my_func()


class Container(object):

    data = Data()

    context = Context()

    _schedule_function_dic = {}

    _handle_data_dic = {}

    current_strategy = None

    @staticmethod
    def set_current_strategy(strategy_name):
        Container.current_strategy = strategy_name
        if strategy_name in Container._schedule_function_dic.keys():
            Container._schedule_function_dic[strategy_name] = None

    @staticmethod
    def register_schedule_function(schedule_func):
        strategy_name = Container.current_strategy
        if strategy_name in Container._schedule_function_dic.keys():
            existing_schedule_functions = Container._schedule_function_dic[strategy_name]
            if existing_schedule_functions is not None:
                Container._schedule_function_dic[strategy_name] = existing_schedule_functions + [schedule_func]
            else:
                Container._schedule_function_dic[strategy_name] = [schedule_func]
        else:
            Container._schedule_function_dic[strategy_name] = [schedule_func]

    @staticmethod
    def register_handle_data(strategy_name, handle_fn):
        Container._handle_data_dic[strategy_name] = lambda: handle_fn(Container.context, Container.data)

    @staticmethod
    def get_schedule_functions(strategy_name):
        return Container._schedule_function_dic[strategy_name]

    @staticmethod
    def get_handle_function(strategy_name):
        return Container._handle_data_dic[strategy_name]


def schedule_function(func, date_rule, time_rule):
    schedule_func = ScheduleFunction(lambda: func(Container.context, Container.data), date_rule, time_rule)
    Container.register_schedule_function(schedule_func)

