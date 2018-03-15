import unittest
from wrapi.data import Data


class IBHistoryTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_count1(self):
        count = Data().history('SPY', 'price', 390, '1m').count()
        self.assertEqual(count, 390)

    def test_count2(self):
        count = Data().history('SPY', 'price', 399, '1m').count()
        self.assertEqual(count, 399)

    def test_first_record(self):
        tradetime = Data().history('SPY', 'price', 390, '1m').first_valid_index().to_pydatetime()
        self.assertEqual(1, tradetime.second)


