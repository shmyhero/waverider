import os
from utils.stringhelper import string_fetch
from wrapi.container import Container
import inspect


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

