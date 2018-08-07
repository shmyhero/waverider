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
        try:
            sub_content = string_fetch(content, 'Currency in USD', 'At close:')
            sub_content = string_fetch(sub_content, 'react-text', 'react-text')
            value = string_fetch(sub_content, '-->', '<!--')
            return float(value.replace(',', ''))
        except Exception:
            sub_content = string_fetch(content, '\"close\":', ',')
            value = round(float(sub_content), 2)
            return value

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


class CNBCScraper(AbstractCurrentDataProvider):

    def __init__(self):
        pass

    def get_data_by_symbol(self, symbol):
        url = 'https://www.cnbc.com/quotes/?symbol=%s' % symbol
        content = HttpHelper.http_get(url)
        value = string_fetch(content, '\"previous_day_closing\":\"', '\"')
        return float(value.replace(',', ''))

    def get_current_data(self, symbols):
        try:
            return map(self.get_data_by_symbol, symbols)
        except Exception as e:
            get_logger().error('Trace: ' + traceback.format_exc(), False)
            get_logger().error('Error: get current price from CNBC failed:' + str(e))
            return None


class SINAScraper(AbstractCurrentDataProvider):

    def __init__(self):
        pass

    def get_data_by_symbols(self, symbols):
        sina_symbols = ','.join(map(lambda x: 'gb_%s' % x.replace('.', '$').lower(), symbols))
        url = 'http://hq.sinajs.cn/?list=%s'%sina_symbols
        content = HttpHelper.http_get(url)
        items = content.split(';')[:-1]
        values = map(lambda x: float(string_fetch(x, ',', ',')), items)
        return values

    def get_data_by_symbol(self, symbol):
        url = 'http://hq.sinajs.cn/?list=gb_%s' % symbol.replace('.', '$').lower()
        content = HttpHelper.http_get(url)
        value = string_fetch(content, ',', ',')
        return float(value)

    def get_current_data(self, symbols):
        try:
            return self.get_data_by_symbols(symbols)
        except Exception as e:
            get_logger().error('Trace: ' + traceback.format_exc(), False)
            get_logger().error('Error: get current price from SINA failed:' + str(e))
            return None


class LaoHu8Scraper(AbstractCurrentDataProvider):

    def __init__(self):
        pass

    def get_data_by_symbol(self, symbol):
        url = 'https://www.laohu8.com/hq/s/%s' % symbol
        content = HttpHelper.http_get(url)
        value = string_fetch(content, 'class=\"price\">', '</td>')
        return float(value)

    def get_current_data(self, symbols):
        try:
            return map(self.get_data_by_symbol, symbols)
        except Exception as e:
            get_logger().error('Trace: ' + traceback.format_exc(), False)
            get_logger().error('Error: get current price from LaoHu8 failed:' + str(e))
            return None


class IBCurrent(AbstractCurrentDataProvider):

    def __init__(self):
        self.api = API()

    def get_data_by_symbol(self, symbol):
        price = self.api.get_market_price(symbol)
        if price < 0:
            raise Exception('The price is negative, price = %s'%price)
        else:
            return price

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
    # print IBCurrent().get_current_data(['SPY', 'SVXY'])
    # print CNBCScraper().get_current_data(['QQQ', 'SVXY'])
    print SINAScraper().get_current_data(['QQQ', 'SVXY', 'LMT','MO','VHT','IHI','MA','V','ITA','CME','IEF','BIL'])
    # print LaoHu8Scraper().get_current_data(['QQQ', 'SVXY'])
