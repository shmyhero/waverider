import traceback
from abc import ABCMeta, abstractmethod
from utils.httphelper import HttpHelper
from utils.stringhelper import string_fetch
from utils.logger import Logger, DailyLoggerFactory
from common.pathmgr import PathMgr
from dataaccess.symbols import Symbols
from ibbasic.api import API


def get_logger():
    return DailyLoggerFactory.get_logger(__name__, PathMgr.get_log_path())


class AbstractCurrentDataProvider(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_current_data(self, symbols):
        pass


class YahooScraper(AbstractCurrentDataProvider):

    def __init__(self):
        pass

    def get_data_by_symbol(self, symbol):
        yahoo_symbol = Symbols.get_mapped_symbol(symbol)
        url = 'https://finance.yahoo.com/quote/%s/' % yahoo_symbol
        get_logger().info('Http request to: %s' % url, False)
        content = HttpHelper.http_get(url)
        content = string_fetch(content, 'Currency in USD', 'At close:')
        content = string_fetch(content, 'react-text', 'react-text')
        value = string_fetch(content, '-->', '<!--')
        return float(value.replace(',', ''))

    def get_current_data(self, symbols):
        try:
            return map(self.get_data_by_symbol, symbols)
        except Exception as e:
            get_logger().error('Trace: ' + traceback.format_exc(), True)
            get_logger().error('Error: get current price from Yahoo failed:' + str(e))
            return None


class MarketWatchScraper(AbstractCurrentDataProvider):

    def __init__(self):
        pass

    def get_data_by_symbol(self, symbol):
        url = 'https://www.marketwatch.com/investing/fund/%s' % symbol
        get_logger().info('Http request to: %s' % url, False)
        content = HttpHelper.http_get(url)
        content = string_fetch(content, 'mw-rangeBar precision=', 'Day Low')
        value = string_fetch(content, '\"last-value\">', '</span>')
        return float(value.replace(',', ''))

    def get_current_data(self, symbols):
        try:
            return map(self.get_data_by_symbol, symbols)
        except Exception as e:
            get_logger().error('Trace: ' + traceback.format_exc(), False)
            get_logger().error('Error: get current price from MarketWatch failed:' + str(e))
            return None


class IBCurrent(AbstractCurrentDataProvider):

    def __init__(self):
        self.api = API()

    def get_data_by_symbol(self, symbol):
        return self.api.get_market_price(symbol)

    def get_current_data(self, symbols):
        try:
            return map(self.get_data_by_symbol, symbols)
        except Exception as e:
            get_logger().error('Trace: ' + traceback.format_exc(), False)
            get_logger().error('Error: get current price from IB failed:' + str(e))
            return None


if __name__ == '__main__':
    # print YahooScraper().get_current_data(['SPX', 'SPY'])
    # print YahooScraper().get_current_data(['YM=F', 'ES=F'])
    # print BarChartScraper().get_current_data(['XIV', 'SVXY'])
    # print MarketWatchScraper().get_current_data(['DJI', 'SPX'])
    # print MarketWatchScraper().get_current_data(['XIV'])
    print IBCurrent().get_current_data(['SPY', 'SVXY'])
