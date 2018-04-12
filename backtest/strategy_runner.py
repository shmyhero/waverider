import datetime
import importlib
import traceback
from common.configmgr import ConfigMgr
from common.tradetime import TradeTime
from backtest.container import Container


class StrategyRunner(object):

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
    def module_patch():
        exec('from backtest.quantopian import schedule_function, date_rules, time_rules, log')
        pass

    @staticmethod
    def init_strategy(strategy_name, logger):
        """
        initialize strategy, it does not support parallel running with same strategy name.
        :param strategy_name:
        :return:
        """
        logger.info('initialize strategy %s...'%strategy_name, False)
        ConfigMgr.for_back_test = True
        s = importlib.import_module('strategies.{}'.format(strategy_name))
        Container.set_current_strategy(strategy_name)
        s.initialize(Container.context)
        if hasattr(s, 'handle_data'):
            Container.register_handle_data(strategy_name, s.handle_data)
        logger.info('initialize strategy %s completed.' % strategy_name, False)

    @staticmethod
    def run_schedule_only(schedule_functions, start_date, end_date, logger):
        for date in StrategyRunner.generate_dates(start_date, end_date):
            sf_dt_list = map(lambda x: [x, x.time_rule.get_datetime(date)], schedule_functions)
            sf_dt_list.sort(key=lambda x: x[1])
            for sf_dt in sf_dt_list:
                if Container.context.terminate_p:
                    return
                schedule_function = sf_dt[0]
                dt = sf_dt[1]
                if schedule_function.date_rule.validate(dt):
                    Container.data.set_datetime(dt)
                    logger.set_dt(dt)
                    try:
                        schedule_function.my_func()
                    except Exception as e:
                        logger.error('Trace: ' + traceback.format_exc(), False)
                        logger.error('Error: get action arguments failed:' + str(e))

    @staticmethod
    def run_schedule_and_handle_function(schedule_functions, handle_function, start_date, end_date, logger):
        for dt in StrategyRunner.generate_datetimes(start_date, end_date):
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
        logger = Container.get_logger(strategy_name)
        StrategyRunner.init_strategy(strategy_name, logger)
        schedule_functions = Container.get_schedule_functions(strategy_name)
        handle_function = Container.get_handle_function(strategy_name)
        if handle_function is None:
            StrategyRunner.run_schedule_only(schedule_functions, start_date, end_date, logger)
        else:
            StrategyRunner.run_schedule_and_handle_function(schedule_functions, handle_function, start_date, end_date, logger)


if __name__ == '__main__':
    # print BackTest.generate_datetimes(datetime.date(2018, 3, 1), datetime.date(2018, 3, 5))
    StrategyRunner.run('caa', datetime.date(2017, 1, 1), datetime.date(2018, 4, 11))