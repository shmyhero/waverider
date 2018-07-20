import sys
import logging
import datetime


class Logger:

    log_file = None
    logger_names = []

    def __init__(self, name, log_path, console=True):
        self.console = console
        self.logger = logging.getLogger(name)
        if log_path:
            self.log_path = log_path
            self.logger.setLevel(logging.INFO)
            self.init_handler(name)
        else:
            self.log_path = None

    def get_formatter(self):
        return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def init_handler(self, name):
        file_path = '%s/%s.log'%(self.log_path, datetime.date.today())
        if Logger.log_file != file_path:
            Logger.log_file = file_path
            Logger.logger_names = []
        if name not in Logger.logger_names:
            fh = logging.FileHandler(file_path)
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter = self.get_formatter()
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            Logger.log_file = file_path
            Logger.logger_names.append(name)

    @property
    def level(self):
        return self.logger.level

    @level.setter
    def level(self, level):
        self.logger.level = level

    def output_console(self, customized_console):
        if customized_console is None:
            return self.console
        else:
            return customized_console

    def info(self, content, console = None):
        if self.output_console(console):
            sys.stdout.write('%s\n'%content)
        if self.log_path:
            self.logger.info(content)

    def error(self, content, console = None):
        if self.output_console(console):
            sys.stderr.write('%s\n'%content)
        if self.log_path:
            self.logger.error(content)

    def warning(self, content, console = None):
        if self.output_console(console):
            sys.stderr.write('%s\n'%content)
        if self.log_path:
            self.logger.warning(content)

    def exception(self, content, console = None):
        if self.output_console(console):
            sys.stderr.write('%s\n'%content)
        if self.log_path:
            self.logger.exception(content)

    def debug(self, content, console = None):
        if self.output_console(console):
            sys.stderr.write('%s\n'%content)
        if self.log_path:
            self.logger.debug(content)


class DailyLoggerFactory(object):

	# BUG: below codes has bug which would lead to no log in new created file...
    # _logger_dic = {}
    # _current_date = datetime.date.today()
    #
    # @staticmethod
    # def get_logger(name, log_path, console=True):
    #     key = "%s%s" % (name, log_path)
    #     if key not in DailyLoggerFactory._logger_dic.keys() or DailyLoggerFactory._current_date != datetime.date.today():
    #         logger = Logger(name, log_path, console)
    #         DailyLoggerFactory._logger_dic[key] = logger
    #         DailyLoggerFactory._current_date = datetime.date.today()
    #         return logger
    #     else:
    #         return DailyLoggerFactory._logger_dic[key]

    @staticmethod
    def get_logger(name, log_path, console=True):
        return Logger(name, log_path, console)