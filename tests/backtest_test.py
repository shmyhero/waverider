import datetime
import unittest
from backtest.strategy_runner import StrategyRunner
from backtest.container import Container
from datasimulation.dataprovider import MontCarloDataProvider


class BackTestTest(unittest.TestCase):

    def test_run_caa(self):
        result = StrategyRunner.run('caa', datetime.date(2017, 12, 29), datetime.date(2018, 2, 12), plot=False)
        self.assertIsNone(result)

    def test_week(self):
        Container.data.provider = MontCarloDataProvider()
        result = StrategyRunner.run('week', datetime.date(2017, 12, 29), datetime.date(2018, 3, 12), plot=False)
        self.assertIsNone(result)