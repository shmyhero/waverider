import os
from utils.stringhelper import string_fetch
from wrapi.container import Container
from date_rules import EveryDayRule, WeekStartRule, WeekEndRule, MonthStartRule, MonthEndRule
from time_rules import MarketOpenRule, MarketCloseRule
import inspect
from wrapi.order import OrderStyle, Order


def schedule_function(func, date_rule, time_rule):
    Container.schedule_function(func, date_rule, time_rule)


class date_rules(object):

    def __init__(self):
        pass

    @staticmethod
    def every_day():
        return EveryDayRule()

    @staticmethod
    def week_start(days_offset=0):
        return WeekStartRule(days_offset)

    @staticmethod
    def week_end(days_offset=0):
        return WeekEndRule(days_offset)

    @staticmethod
    def month_start(days_offset=0):
        return MonthStartRule(days_offset)

    @staticmethod
    def month_end(days_offset=0):
        return MonthEndRule(days_offset)


class time_rules(object):

    def __init__(self):
        pass

    @staticmethod
    def market_open(hours=0, minutes=1):
        return MarketOpenRule(hours, minutes)

    @staticmethod
    def market_close(hours=0, minutes=1):
        return MarketCloseRule(hours, minutes)


def order_target(asset, amount, style=OrderStyle.MarketOrder, sec_type='STK'):
    return Order.order_target(asset, amount, style, sec_type)


def order_target_percent(asset, percent, style=OrderStyle.MarketOrder, sec_type = 'STK'):
    return Order.order_target_percent(asset, percent, style, sec_type)


def get_open_orders(asset=None):
    return Order.get_open_orders(asset)


def cancel_order(order_id):
    Order.cancel_order(order_id)


def set_stop_price(asset, stop_price):
    return Order.set_stop_price(asset, stop_price)


def symbol(asset):
    return asset


def symbols(*args):
    return list(args)


class log(object):

    @staticmethod
    def get_logger():
        frame = inspect.stack()[2]
        the_module = inspect.getmodule(frame[0])
        filename = the_module.__file__
        strategy_name = string_fetch(os.path.split(filename)[1], '', '.')
        return Container.get_logger(strategy_name=strategy_name)

    @staticmethod
    def info(content):
        log.get_logger().info(content)

    @staticmethod
    def error(content):
        log.get_logger().error(content)

    @staticmethod
    def warning(content):
        log.get_logger().warning(content)

    @staticmethod
    def exception(content):
        log.get_logger().exception(content)

