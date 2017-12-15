import datetime
import time
import importlib
import traceback
from multiprocessing import Process
from utils.logger import Logger
from common.pathmgr import PathMgr
from common.tradetime import TradeTime
from wrapi.container import Container


class StrategyRunner(object):

    logger = Logger(__name__, PathMgr.get_log_path())

    _running_strategies = []

    @staticmethod
    def init_strategy(strategy_name):
        """
        initialize strategy, it does not support parallel running with same strategy name.
        :param strategy_name:
        :return:
        """
        StrategyRunner.logger.info('initialize strategy %s...'%strategy_name, False)
        s = importlib.import_module('strategies.{}'.format(strategy_name))
        Container.set_current_strategy(strategy_name)
        s.initialize(Container.context)
        if hasattr(s, 'handle_data'):
            Container.register_handle_data(strategy_name, s.handle_data)
        StrategyRunner.logger.info('initialize strategy %s completed.' % strategy_name, False)

    @staticmethod
    def listener(strategy_name):
        schedule_functions = Container.get_schedule_functions(strategy_name)
        handle_function = Container.get_handle_function(strategy_name)
        start_time = None
        while True:
            start_time = start_time or datetime.datetime.now()
            StrategyRunner.logger.info('check schedule functions....')
            for schedule_function in schedule_functions:
                try:
                    schedule_function.run(start_time)
                except Exception as e:
                    StrategyRunner.logger.error('Trace: ' + traceback.format_exc(), False)
                    StrategyRunner.logger.error('Error: get action arguments failed:' + str(e))
            if handle_function is not None:
                StrategyRunner.logger.info('check handle functions....')
                try:
                    handle_function()
                except Exception as e:
                    StrategyRunner.logger.error('Trace: ' + traceback.format_exc(), False)
                    StrategyRunner.logger.error('Error: get action arguments failed:' + str(e))
            end_time = datetime.datetime.now()
            next_start_time = datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour,
                                                start_time.minute, 0, ) + datetime.timedelta(minutes=1)
            # print 'start_time=%s, end_time=%s, delta=%s' % (start_time, end_time, end_time-start_time)
            if (end_time - start_time) < datetime.timedelta(minutes=1):
                # print 'next_start_time=%s'%next_start_time
                interval = (next_start_time - datetime.datetime.now()).total_seconds()
                # print 'interval=%s'%interval
                if interval > 0:
                    time.sleep(interval)
            else:
                StrategyRunner.logger.warning('your function runs exceed 1 minutes')
            start_time = next_start_time

    @staticmethod
    def run(strategy_name):
        """
        it can support parallel running for different strategies, however, multiple strategies may lead to too frequency
        to call the IB API, the IB API doesn't support multiple thread/process, it may failed if 2 strategy call IB API
        at the same time or in short time interval.
        if we want to debug it, do not use multiple process.
        :param strategy_name:
        :return:
        """
        if strategy_name not in StrategyRunner._running_strategies:
            StrategyRunner._running_strategies.append(strategy_name)
            StrategyRunner.init_strategy(strategy_name)
            StrategyRunner.logger.info('run strategy %s ...' % strategy_name)
            # p = Process(target=StrategyRunner.listener, args=(strategy_name,))
            # p.start()
            StrategyRunner.listener(strategy_name)
        else:
            StrategyRunner.logger.info('Strategy %s is already running...' % strategy_name)


if __name__ == '__main__':
    #pass
    StrategyRunner.run('b')
    #time.sleep(5)
    #StrategyRunner.run_strategy_in_real_time('b')


