import unittest
import time
from wrapi.quantopian import order_target, order_target_percent, get_open_orders, cancel_order, set_stop_price


class OrderTest(unittest.TestCase):

    def setUp(self):
        self.order_id_lst = []

    def tearDown(self):
        time.sleep(2)
        open_orders = get_open_orders().index.values
        for order_id in self.order_id_lst:
            if order_id in open_orders:
                cancel_order(order_id)

    def test_order_target(self):
        order_id = order_target('SPY', 10)
        self.order_id_lst.append(order_id)
        order_ids = get_open_orders().index.values
        flag = order_id in order_ids
        self.assertTrue(flag)

    def test_order_target_percent(self):
        order_id = order_target_percent('QQQ', 0.01)
        self.order_id_lst.append(order_id)
        order_ids = get_open_orders().index.values
        flag = order_id in order_ids
        self.assertTrue(flag)
        cancel_order(order_id)
        order_ids = get_open_orders().index.values
        flag = order_id in order_ids
        self.assertFalse(flag)
        if flag is False:
            self.order_id_lst.remove(order_id)

    def test_too_much_order(self):
        with self.assertRaises(Exception) as context:
            order_target('SPY', 1000000000)
            self.assertTrue('Invalid value in field' in context.exception)

    def test_too_much_order2(self):
        with self.assertRaises(Exception) as context:
            order_target_percent('QQQ', 2)
            self.assertTrue('The cost of asset exceed total cash' in context.exception)

    def verify_stop_order(self):
        order_id = set_stop_price('SPY', 255)
        self.order_id_lst.append(order_id)
        order_ids = get_open_orders().index.values
        flag = order_id in order_ids
        self.assertTrue(flag)








