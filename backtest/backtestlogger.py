import datetime
import logging
from utils.logger import Logger, DailyLoggerFactory


class BackTestLogger(Logger):

    def __init__(self, log_path, console=True):
        Logger.__init__(self, __name__, log_path, console)
        self.current_datetime = datetime.datetime.now()

    def set_dt(self, dt):
        self.current_datetime = dt

    def get_formatter(self):
        return logging.Formatter('%(levelname)s - %(message)s')

    def decorate_message(self, content):
        return "%s - %s" % (self.current_datetime.strftime('%Y-%m-%d %H:%M'), content)

    def info(self, content, console = None):
        Logger.info(self, self.decorate_message(content), console)

    def error(self, content, console = None):
        Logger.error(self, self.decorate_message(content), console)

    def warning(self, content, console = None):
        Logger.warning(self, self.decorate_message(content), console)

    def exception(self, content, console = None):
        Logger.exception(self, self.decorate_message(content), console)

    def debug(self, content, console = None):
        Logger.debug(self, self.decorate_message(content), console)


class DailyBackTestLoggerFactory(object):

    _logger_dic = {}
    _current_date = datetime.date.today()

    @staticmethod
    def get_logger(log_path, console=True):
        key = log_path
        if key not in DailyBackTestLoggerFactory._logger_dic.keys() or DailyBackTestLoggerFactory._current_date != datetime.date.today():
            logger = BackTestLogger(log_path, console)
            DailyBackTestLoggerFactory._logger_dic[key] = logger
            DailyLoggerFactory._current_date = datetime.date.today()
            return logger
        else:
            return DailyBackTestLoggerFactory._logger_dic[key]