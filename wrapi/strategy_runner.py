import datetime
import time
import importlib
from multiprocessing import Process
from wrapi.container import Container


class StrategyRunner(object):

    running_strategies = []

    @staticmethod
    def init_strategy(strategy_name):
        """
        initialize strategy, it does not support parallel running with same strategy name.
        :param strategy_name:
        :return:
        """
        s = importlib.import_module('strategies.{}'.format(strategy_name))
        Container.set_current_strategy(strategy_name)
        s.initialize(Container.context)
        Container.register_handle_data(strategy_name, s.handle_data)

    @staticmethod
    def listener(strategy_name):
        schedule_functions = Container.get_schedule_functions(strategy_name)
        handle_function = Container.get_handle_function(strategy_name)
        start_time = None
        while True:
            start_time = start_time or datetime.datetime.now()
            for schedule_function in schedule_functions:
                schedule_function.run(start_time)
            handle_function()
            end_time = datetime.datetime.now()
            next_start_time = datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour,
                                                start_time.minute, 0) + datetime.timedelta(minutes=1)
            if (end_time - start_time) < datetime.timedelta(minutes=1):
                interval = (next_start_time - datetime.datetime.now()).total_seconds()
                if interval > 0:
                    time.sleep(interval)
            else:
                # TODO: logger.warn('your function runs exceed 1 minutes')
                pass
            start_time = next_start_time

    @staticmethod
    def run_strategy(strategy_name):
        """
        it can support parallel running for different strategy, however, multiple strategies may lead to too frequency
        to call the IB API, the IB API doesn't support multiple thread/process, it may failed if 2 strategy call IB API
        at the same time or in short time interval...
        :param strategy_name:
        :return:
        """
        if strategy_name not in StrategyRunner.running_strategies:
            StrategyRunner.running_strategies.append(strategy_name)
            StrategyRunner.init_strategy(strategy_name)
            p = Process(target=StrategyRunner.listener, args=(strategy_name,))
            p.start()
            # StrategyRunner.listener(strategy_name)


if __name__ == '__main__':
    pass
    #StrategyRunner.run_strategy('a')
    #time.sleep(5)
    #StrategyRunner.run_strategy('b')


