import datetime
import time
import importlib
import traceback
from utils.logger import Logger, DailyLoggerFactory
from common.pathmgr import PathMgr
from common.tradetime import TradeTime
from wrapi.container import Container


class StrategyRunner(object):

    _running_strategies = []

    @staticmethod
    def get_logger():
        return DailyLoggerFactory.get_logger(__name__, PathMgr.get_log_path())

    @staticmethod
    def init_strategy(strategy_name):
        """
        initialize strategy, it does not support parallel running with same strategy name.
        :param strategy_name:
        :return:
        """
        logger = StrategyRunner.get_logger()
        logger.info('initialize strategy %s...'%strategy_name, False)
        s = importlib.import_module('strategies.{}'.format(strategy_name))
        Container.set_current_strategy(strategy_name)
        s.initialize(Container.context)
        if hasattr(s, 'handle_data'):
            Container.register_handle_data(strategy_name, s.handle_data)
        logger.info('initialize strategy %s completed.' % strategy_name, False)

    @staticmethod
    def listener(strategy_name, market_open_only=True):
        """
        :param strategy_name:
        :param market_open_only:
          if you want handle function run every minutes, even if the market is not open, give it false.
        :return:
        """
        schedule_functions = Container.get_schedule_functions(strategy_name)
        handle_function = Container.get_handle_function(strategy_name)
        last_minute = datetime.datetime.now().minute-1
        while True:
            if Container.context.terminate_p:
                break
            now = datetime.datetime.now()
            if now.minute == last_minute:
                time.sleep(1)
                continue
            else:
                logger = StrategyRunner.get_logger()
                # logger.info('check schedule functions...')
                for schedule_function in schedule_functions:
                    try:
                        schedule_function.run(now)
                    except Exception as e:
                        logger.error('Trace: ' + traceback.format_exc(), False)
                        logger.error('Error: get action arguments failed:' + str(e))
                if handle_function is not None:
                    # logger.info('check handle functions...')
                    if market_open_only is False or TradeTime.is_market_open():
                        try:
                            handle_function()
                        except Exception as e:
                            logger.error('Trace: ' + traceback.format_exc(), False)
                            logger.error('Error: get action arguments failed:' + str(e))
                    else:
                        # logger.info('market not open...')
                        Container.clear_loggers()
                last_minute = now.minute

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
            StrategyRunner.get_logger().info('run strategy %s ...' % strategy_name)
            # if we are change multiple process, we would use below codes.
            # p = Process(target=StrategyRunner.listener, args=(strategy_name,))
            # p.start()
            StrategyRunner.listener(strategy_name)
            # if you want handle function run every minutes, even if the market is not open, give it false.
            # StrategyRunner.listener(strategy_name, False)
        else:
            StrategyRunner.get_logger().info('Strategy %s is already running...' % strategy_name)


if __name__ == '__main__':
    #pass
    StrategyRunner.run('a')
    #time.sleep(5)
    #StrategyRunner.run_strategy_in_real_time('b')

