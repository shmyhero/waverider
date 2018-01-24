import json
import traceback
from abc import ABCMeta, abstractmethod
from datetime import datetime
from utils.httphelper import HttpHelper
from utils.stringhelper import string_fetch
from utils.logger import Logger
from dataaccess.symbols import Symbols


class WebScraper(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_current_data(self, symbols):
        pass


class YahooScraper(WebScraper):

    def __init__(self, logger=Logger(__name__, None)):
        self.logger = logger

    def get_data_by_symbol(self, symbol):
        yahoo_symbol = Symbols.get_mapped_symbol(symbol)
        url = 'https://finance.yahoo.com/quote/%s/' % yahoo_symbol
        self.logger.info('Http request to: %s' % url, False)
        content = HttpHelper.http_get(url)
        content = string_fetch(content, 'Currency in USD', 'At close:')
        content = string_fetch(content, 'react-text', 'react-text')
        value = string_fetch(content, '-->', '<!--')
        return float(value.replace(',', ''))

    def get_current_data(self, symbols):
        try:
            return map(self.get_data_by_symbol, symbols)
        except Exception as e:
            self.logger.error('Trace: ' + traceback.format_exc(), True)
            self.logger.error('Error: get current price from Yahoo failed:' + str(e))
            return None


class MarketWatchScraper(WebScraper):

    def __init__(self, logger=Logger(__name__, None)):
        self.logger = logger

    def get_data_by_symbol(self, symbol):
        url = 'https://www.marketwatch.com/investing/fund/%s' % symbol
        self.logger.info('Http request to: %s' % url, False)
        content = HttpHelper.http_get(url)
        content = string_fetch(content, 'mw-rangeBar precision=', 'Day Low')
        value = string_fetch(content, '\"last-value\">', '</span>')
        return float(value.replace(',', ''))

    def get_current_data(self, symbols):
        try:
            return map(self.get_data_by_symbol, symbols)
        except Exception as e:
            self.logger.error('Trace: ' + traceback.format_exc(), False)
            self.logger.error('Error: get current price from MarketWatch failed:' + str(e))
            return None


if __name__ == '__main__':
    # print YahooScraper().get_current_data(['SPX', 'SPY'])
    print YahooScraper().get_current_data(['YM=F', 'ES=F'])
    # print BarChartScraper().get_current_data(['XIV', 'SVXY'])
    # print MarketWatchScraper().get_current_data(['DJI', 'SPX'])
    #print MarketWatchScraper().get_current_data(['XIV'])
