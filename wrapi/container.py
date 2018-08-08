import datetime
import pytz
from utils.logger import DailyLoggerFactory, Logger
from utils.timezonehelper import convert_to_us_east_dt
from common.tradetime import TradeTime
from common.pathmgr import PathMgr
from wrapi.context import Context
from wrapi.data import Data
from wrapi.analysis import PortfolioDAO
from wrapi.date_rules import EveryDayRule
from wrapi.time_rules import MarketCloseRule


class ScheduleFunction(object):

    def __init__(self, my_func, date_rule, time_rule, half_days=True):
        self.my_func = my_func
        self.date_rule = date_rule
        self.time_rule = time_rule
        self.half_days = half_days

    def run(self, current_time):
        dt = convert_to_us_east_dt(current_time)
        # if you want to run the schedule function immediately,
        # you would need to add below 2 line code, given the correct time interval.
        # dt += datetime.timedelta(hours=12, minutes=33)
        # print dt
        if TradeTime.is_half_trade_day(dt.date()) and self.half_days is False:
            return
        if self.date_rule.validate(dt) and self.time_rule.validate(dt):
            self.my_func()


class Container(object):
    """ this class does not support run multiple strategies in parallel"""

    data = Data()

    context = Context()

    current_strategy = None

    _schedule_function_dic = {}

    _handle_data_dic = {}

    # strategies_logger_dic should be clear after market close..
    _strategies_logger_dic = {}


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
        global_schedule_functions = [ScheduleFunction(lambda: PortfolioDAO.save_portfolio_info(strategy_name), EveryDayRule(), MarketCloseRule(-4))]
        return Container._schedule_function_dic[strategy_name] + global_schedule_functions

    @staticmethod
    def get_handle_function(strategy_name):
        if strategy_name in Container._handle_data_dic.keys():
            return Container._handle_data_dic[strategy_name]
        else:
            return None

    @staticmethod
    def get_logger(strategy_name):
        if strategy_name not in Container._strategies_logger_dic.keys():
            logger = Logger(strategy_name, PathMgr.get_log_path(strategy_name), True)
            Container._strategies_logger_dic[strategy_name] = logger
        return Container._strategies_logger_dic[strategy_name]

    @staticmethod
    def clear_loggers():
        Container._strategies_logger_dic = {}

    @staticmethod
    def schedule_function(func, date_rule, time_rule, half_days=True):
        schedule_func = ScheduleFunction(lambda: func(Container.context, Container.data), date_rule, time_rule, half_days)
        Container.register_schedule_function(schedule_func)

