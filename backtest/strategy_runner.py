import datetime
import importlib
import traceback
from common.configmgr import ConfigMgr
from common.tradetime import TradeTime
from backtest.container import Container
from backtest.api import API


class StrategyRunner(object):

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
        for date in TradeTime.generate_dates(start_date, end_date):
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
                        start = datetime.datetime.now()
                        schedule_function.my_func()
                        end = datetime.datetime.now()
                        # logger.info('Spend time for schedule function: %s seconds' % (end - start).seconds)
                    except Exception as e:
                        logger.error('Trace: ' + traceback.format_exc(), False)
                        logger.error('Error: get action arguments failed: %s, %s' % (str(e), traceback.format_exc()))
            Container.data.set_datetime(datetime.datetime(date.year, date.month, date.day, 16, 0, 0))
            Container.analysis.add_portfolio_trace(date, Container.api.portfolio)

    @staticmethod
    def run_schedule_and_handle_function(schedule_functions, handle_function, start_date, end_date, logger):
        for dt in TradeTime.generate_datetimes(start_date, end_date):
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
            if dt.minute == 0:
                if (TradeTime.is_half_trade_day(dt.date()) and dt.hour == 13) or dt.hour == 16:
                    Container.analysis.add_portfolio_trace(dt.date(), Container.api.portfolio)

    @staticmethod
    def run(strategy_name, start_date, end_date, initial_fund=None, plot=True):
        if initial_fund is not None:
            Container.api = API(Container.data, initial_fund)
        logger = Container.get_logger(strategy_name)
        StrategyRunner.init_strategy(strategy_name, logger)
        schedule_functions = Container.get_schedule_functions(strategy_name)
        handle_function = Container.get_handle_function(strategy_name)
        if handle_function is None:
            StrategyRunner.run_schedule_only(schedule_functions, start_date, end_date, logger)
        else:
            StrategyRunner.run_schedule_and_handle_function(schedule_functions, handle_function, start_date, end_date, logger)
        Container.analysis.calc_stats()
        if plot:
            Container.analysis.plot()


if __name__ == '__main__':
    # print BackTest.generate_datetimes(datetime.date(2018, 3, 1), datetime.date(2018, 3, 5))
    start = datetime.datetime.now()
    # from datasimulation.dataprovider import MontCarloDataProvider
    # Container.data.provider = MontCarloDataProvider()
    StrategyRunner.run('macdspy', datetime.date(2018, 4, 1), datetime.date(2018, 4, 30))
    end = datetime.datetime.now()
    print (end-start).seconds
