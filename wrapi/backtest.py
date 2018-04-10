import datetime
import traceback
import importlib
from backtestlogger import DailyBackTestLoggerFactory
from common.pathmgr import PathMgr
from common.tradetime import TradeTime
from wrapi.container import Container
from wrapi.data import BackTestData


class BackTest(object):

    @staticmethod
    def generate_dates(from_date, end_date):
        dates = []
        current_date = from_date
        while current_date <= end_date:
            if TradeTime.is_trade_day(current_date):
                start_date = datetime.date(current_date.year, current_date.month, current_date.day)
                dates.append(start_date)
            current_date += datetime.timedelta(days=1)
        return dates

    @staticmethod
    def generate_datetimes(from_date, end_date):
        datetimes = []
        current_date = from_date
        while current_date <= end_date:
            if TradeTime.is_trade_day(current_date):
                start_time = datetime.datetime(current_date.year, current_date.month, current_date.day, 9, 31, 0)
                if TradeTime.is_half_trade_day(current_date):
                    count = 180
                else:
                    count = 390
                for i in range(count):
                    datetimes.append(start_time + datetime.timedelta(minutes=i))
            current_date += datetime.timedelta(days=1)
        return datetimes

    @staticmethod
    def init_strategy(strategy_name, logger):
        """
        initialize strategy, it does not support parallel running with same strategy name.
        :param strategy_name:
        :return:
        """
        logger.info('initialize strategy %s...'%strategy_name, False)
        s = importlib.import_module('strategies.{}'.format(strategy_name))
        Container.set_current_strategy(strategy_name)
        s.initialize(Container.context)
        if hasattr(s, 'handle_data'):
            Container.register_handle_data(strategy_name, s.handle_data)
        logger.info('initialize strategy %s completed.' % strategy_name, False)

    @staticmethod
    def run_schedule_only(schedule_functions, start_date, end_date, logger):
        for date in BackTest.generate_dates(start_date, end_date):
            sf_dt_list = map(lambda x: [x, x.time_rule.get_datetime(date)], schedule_functions)
            sf_dt_list.sort(key=lambda x: x[1])
            for sf_dt in sf_dt_list:
                if Container.context.terminate_p:
                    return
                schedule_function = sf_dt[0]
                dt = sf_dt[1]
                Container.data.set_datetime(dt)
                logger.set_dt(dt)
                try:
                    schedule_function.my_func()
                except Exception as e:
                    logger.error('Trace: ' + traceback.format_exc(), False)
                    logger.error('Error: get action arguments failed:' + str(e))

    @staticmethod
    def run_schedule_and_handle_function(schedule_functions, handle_function, start_date, end_date, logger):
        for dt in BackTest.generate_datetimes(start_date, end_date):
            if Container.context.terminate_p:
                return
            Container.data.set_datetime(dt)
            logger.set_dt(dt)
            for schedule_function in schedule_functions:
                try:
                    schedule_function.run(dt)
                except Exception as e:
                    logger.error('Trace: ' + traceback.format_exc(), False)
                    logger.error('Error: get action arguments failed:' + str(e))
            try:
                handle_function()
            except Exception as e:
                logger.error('Trace: ' + traceback.format_exc(), False)
                logger.error('Error: get action arguments failed:' + str(e))

    @staticmethod
    def run(strategy_name, start_date, end_date):
        Container.data = BackTestData()
        logger = Container.get_logger(strategy_name)
        BackTest.init_strategy(strategy_name, logger)
        schedule_functions = Container.get_back_test_schedule_functions(strategy_name)
        handle_function = Container.get_handle_function(strategy_name)
        if handle_function is None:
            BackTest.run_schedule_only(schedule_functions, start_date, end_date, logger)
        else:
            BackTest.run_schedule_and_handle_function(schedule_functions, handle_function, start_date, end_date, logger)


if __name__ == '__main__':
    # print BackTest.generate_datetimes(datetime.date(2018, 3, 1), datetime.date(2018, 3, 5))
    BackTest.run('b', datetime.date(2018, 4, 1), datetime.date(2018, 4, 5))