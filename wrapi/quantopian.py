import os
from utils.stringhelper import string_fetch
from wrapi.container import Container
from date_rules import EveryDayRule, WeekStartRule, WeekEndRule, MonthStartRule, MonthEndRule
from time_rules import MarketOpenRule, MarketCloseRule
import inspect
from wrapi.order import OrderStyle, Order


def schedule_function(func, date_rule, time_rule):
    """
    We provide the schedule_function method that lets your algorithm specify
    when methods are run by using date and/or time rules.
    All scheduling must be done from within the initialize method.
    :param func: a function with context and data parameters.
    :param date_rule: date rule for triggering schedule function, please refer to data_rules class.
    :param time_rule: time rule for triggering schedule function, please refer to time_rules class.
    :return:
    """
    Container.schedule_function(func, date_rule, time_rule)


class date_rules(object):
    """
    date rules for triggering schedule function.
    """

    def __init__(self):
        pass

    @staticmethod
    def every_day():
        """
        schedule function run every day
        :return:
        """
        return EveryDayRule()

    @staticmethod
    def week_start(days_offset=0):
        """
         accept a days_offset parameter to offset the function execution by a specific number of trading days from
         the beginning of the week
        :param days_offset:
        :return:
        """
        return WeekStartRule(days_offset)

    @staticmethod
    def week_end(days_offset=0):
        """
        accept a days_offset parameter to offset the function execution by a specific number of trading days from
        the end of the week
        :param days_offset:
        :return:
        """
        return WeekEndRule(days_offset)

    @staticmethod
    def month_start(days_offset=0):
        """
        accept a days_offset parameter to offset the function execution by a specific number of trading days from
        the beginning of the month
        :param days_offset:
        :return:
        """
        return MonthStartRule(days_offset)

    @staticmethod
    def month_end(days_offset=0):
        """
        accept a days_offset parameter to offset the function execution by a specific number of trading days from
        the end of the month
        :param days_offset:
        :return:
        """
        return MonthEndRule(days_offset)


class time_rules(object):
    """
    time rules for triggering schedule function.
    """

    def __init__(self):
        pass

    @staticmethod
    def market_open(hours=0, minutes=1):
        """
        Specifies the time portion of the schedule.
        This can be set as market_open and has an offset parameter to indicate
        how many hours or minutes from the market open.
        The default is 1 minute after market open.
        :param hours: hours after market open.
        :param minutes: minutes after market open.
        :return:
        """
        return MarketOpenRule(hours, minutes)

    @staticmethod
    def market_close(hours=0, minutes=1):
        """
        Specifies the time portion of the schedule.
        This can be set as  market_close and has an offset parameter to
        indicate how many hours or minutes from the market close.
        The default is  1 minute before market close.
        :param hours: hours before market close
        :param minutes: minutes before market close
        :return:
        """
        return MarketCloseRule(hours, minutes)


def order_target(asset, amount, style=OrderStyle.MarketOrder, sec_type='STK'):
    """
    Places an order to a target number of shares.
    Placing a negative target order will result in a short position equal to the negative number specified.
    :param asset: a string identity for the asset
    :param amount: the quantity of asset
    :param style: market price in default, it can also be a limit order
    :param sec_type: The security type for the contract ('STK' is 'stock'), it can be 'OPT' or 'CASH'
    :return:order id
    """
    return Order.order_target(asset, amount, style, sec_type)


def order_target_percent(asset, percent, style=OrderStyle.MarketOrder, sec_type='STK'):
    """
    Place an order to adjust a position to a target percent of the current portfolio value.
    If there is no existing position in the asset, an order is placed for the full target percentage.
    If there is a position in the asset, an order is placed for the difference between the target percent
    and the current percent.
    Placing a negative target percent order will result in a short position equal to the negative target percent.
    Portfolio value is calculated as the sum of the positions value and ending cash balance.
    Orders are always truncated to whole shares, and percentage must be expressed as a decimal (0.50 means 50%).
    :param asset: a string identity for the asset
    :param percent: the percentage of current portfolio value
    :param style: market price in default, it can also be a limit order
    :param sec_type: he security type for the contract ('STK' is 'stock'), it can be 'OPT' or 'CASH'
    :return: order id
    """
    return Order.order_target_percent(asset, percent, style, sec_type)


def get_open_orders(asset=None):
    """
    Return a dataframe for orders, If asset is None or not specified, returns all open orders.
    If asset is specified, returns open orders for that asset
    :param asset: filter the open orders by specified asset
    :return: a dataframe for open orders
    """
    return Order.get_open_orders(asset)


def cancel_order(order_id):
    """
    cancel the open order.
    :param order_id: order id need to get order id by calling get_open_orders function,
    order_target or order_target_percent function.
    :return:
    :exception: order not found
    """
    Order.cancel_order(order_id)


def set_stop_price(asset, stop_price):
    """
    set stop price with OrderStyle.StopOrder. need to specify asset and  stop price,
    the quantity is the current amount of the specified symbol in position
    :param asset: a string identity for the asset
    :param stop_price: stop price for asset
    :return: order id
    """
    return Order.set_stop_price(asset, stop_price)


def symbol(asset):
    """
    return the value of asset, in order to be compatible with quantopian.
    :param asset:
    :return: assert
    """
    return asset


def symbols(*args):
    """
    convert *args to a list
    i.e.: ('SPY', 'QQQ') => ['SPY', 'QQQ']
    :param args: assets
    :return: the list of assets
    """
    return list(args)


class log(object):
    """
    adapter to logger in waverider
    """

    @staticmethod
    def get_logger():
        frame = inspect.stack()[2]
        the_module = inspect.getmodule(frame[0])
        filename = the_module.__file__
        strategy_name = string_fetch(os.path.split(filename)[1], '', '.')
        return Container.get_logger(strategy_name=strategy_name)

    @staticmethod
    def get_error_logger():
        frame = inspect.stack()[2]
        the_module = inspect.getmodule(frame[0])
        filename = the_module.__file__
        strategy_name = string_fetch(os.path.split(filename)[1], '', '.')
        return Container.get_logger(strategy_name='%s_error' % strategy_name)

    @staticmethod
    def info(content):
        log.get_logger().info(content)

    @staticmethod
    def error(content):
        log.get_logger().error(content)
        log.get_error_logger().error(content, False)

    @staticmethod
    def warning(content):
        log.get_logger().warning(content)
        log.get_error_logger().warning(content, False)

    @staticmethod
    def exception(content):
        log.get_logger().exception(content)
        log.get_error_logger().exception(content, False)

