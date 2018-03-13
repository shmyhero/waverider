import datetime
import pytz
from utils.logger import DailyLoggerFactory
from common.pathmgr import PathMgr
from wrapi.context import Context
from wrapi.data import Data
from wrapi.analysis import PortfolioDAO
from wrapi.date_rules import EveryDayRule
from wrapi.time_rules import MarketCloseRule


class ScheduleFunction(object):

    def __init__(self, my_func, date_rule, time_rule):
        self.my_func = my_func
        self.date_rule = date_rule
        self.time_rule = time_rule

    def run(self, current_time):
        native_dt = datetime.datetime.now()
        us_dt = datetime.datetime.now(pytz.timezone('US/Eastern'))
        delta_hour = datetime.datetime(native_dt.year, native_dt.month, native_dt.day, native_dt.hour, native_dt.minute, 0) - datetime.datetime(us_dt.year, us_dt.month, us_dt.day, us_dt.hour, us_dt.minute, 0)
        dt = current_time - delta_hour
        # if you want to run the schedule function immediately,
        # you would need to add below 2 line code, given the correct time interval.
        # dt += datetime.timedelta(hours=12, minutes=33)
        # print dt
        if self.date_rule.validate(dt) and self.time_rule.validate(dt):
            self.my_func()


class Container(object):
    """ this class does not support run multiple strategies in parallel"""

    data = Data()

    context = Context()

    current_strategy = None

    _schedule_function_dic = {}

    _handle_data_dic = {}

    @staticmethod
    def set_current_strategy(strategy_name):
        Container.current_strategy = strategy_name
        Container.context.strategy_name = strategy_name
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
        global_schedule_functions = [ScheduleFunction(lambda : PortfolioDAO.save_portfolio_info(strategy_name), EveryDayRule(), MarketCloseRule(-4))]
        return Container._schedule_function_dic[strategy_name] + global_schedule_functions

    @staticmethod
    def get_handle_function(strategy_name):
        if strategy_name in Container._handle_data_dic.keys():
            return Container._handle_data_dic[strategy_name]
        else:
            return None

    @staticmethod
    def get_logger(strategy_name):
        return DailyLoggerFactory.get_logger(strategy_name, PathMgr.get_log_path(strategy_name))

    @staticmethod
    def schedule_function(func, date_rule, time_rule):
        schedule_func = ScheduleFunction(lambda: func(Container.context, Container.data), date_rule, time_rule)
        Container.register_schedule_function(schedule_func)

