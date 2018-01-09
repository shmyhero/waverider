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
    def get_current_data(self):
        pass


class YahooScraper(WebScraper):

    def __init__(self, logger=Logger(__name__, None)):
        self.logger = logger

    @staticmethod
    def parse_value(str_value, value_type):
        if str_value == 'N/A' or str_value == '':
            return None
        if value_type == 'float':
            return float(str_value)
        if value_type == 'int':
            return int(str_value)
        if value_type == 'date':
            return datetime.strptime(str_value.replace('\"', ''), "%m/%d/%Y")
        else:
            return None

    @staticmethod
    def parse_record(record):
        values = record.split(',')
        if len(values) < 6:
            return [None, None, None, None, None, None]
        result = [YahooScraper.parse_value(values[0], 'float'),
                  YahooScraper.parse_value(values[1], 'float'),
                  YahooScraper.parse_value(values[2], 'float'),
                  YahooScraper.parse_value(values[3], 'float'),
                  YahooScraper.parse_value(values[4], 'int'),
                  YahooScraper.parse_value(values[5], 'date')]
        return result

    def get_current_data(self, symbols):
        yahoo_symbols = map(lambda x: Symbols.get_mapped_symbol(x, Symbols.YahooSymbolMapping), symbols)
        url_template = 'http://finance.yahoo.com/d/quotes.csv?s={}&f=ol1hgvd1'
        url = url_template.format(','.join(yahoo_symbols))
        # print url
        content = ''
        try:
            content = HttpHelper.http_get(url)
        except Exception as e:
            self.logger.error('Trace: ' + traceback.format_exc(), False)
            self.logger.error('Error: get action arguments failed:' + str(e))
        # print content
        records = content.split('\n')[:-1]
        return map(YahooScraper.parse_record, records)


class BarChartScraper(WebScraper):

    def __init__(self, logger=Logger(__name__, None)):
        self.logger = logger

    def parse_content(self, content):
        try:
            json_data = json.loads(content)
            for record in json_data['results']:
                yield [record['open'], record['close'], record['high'], record['low'], record['volume'],
                       datetime.strptime(record['tradeTimestamp'][0:10], '%Y-%m-%d')]
        except Exception as e:
            self.logger.error('Trace: ' + traceback.format_exc(), False)
            self.logger.error('Error: get action arguments failed:' + str(e))
            yield [None, None, None, None, None, None]

    def get_current_data(self, symbols):
        url_template = "http://marketdata.websol.barchart.com/getQuote.json?apikey=7aa9a38e561042d48e32f3b469b730d8&symbols={}"
        url = url_template.format(','.join(symbols))
        # print url
        try:
            content = HttpHelper.http_get(url)
        except Exception as e:
            self.logger.error('Trace: ' + traceback.format_exc(), False)
            self.logger.error('Error: get action arguments failed:' + str(e))
            content = ''
        # print content
        return list(self.parse_content(content))


class MarketWatchScraper(WebScraper):

    def __init__(self, logger=Logger(__name__, None)):
        self.logger = logger

    def get_prices(self, url):
        content = HttpHelper.http_get(url)
        # print content
        sub_content = string_fetch(content, 'mw-rangeBar precision=', 'Day Low')
        # print sub_content
        open = float(string_fetch(sub_content, 'day-open=\"', '\"'))
        close = float(string_fetch(sub_content, '\"last-value\">', '</span>'))
        high = float(string_fetch(sub_content, 'range-high=\"', '\"'))
        low = float(string_fetch(sub_content, 'range-low=\"', '\"'))
        return [open, close, high, low]

    def get_symbol_data(self, symbol):
        url = 'https://www.marketwatch.com/investing/fund/%s' % symbol
        record = [None, None, None, None]
        try:
            record = self.get_prices(url)
        except Exception as e:
            self.logger.error('Trace: ' + traceback.format_exc(), False)
            self.logger.error('Error: get action arguments failed:' + str(e))
        return record + [None, None] # volumn and tradetime are None

    def get_current_data(self, symbols):
        return map(self.get_symbol_data, symbols)


if __name__ == '__main__':
    #print YahooScraper().get_current_data(['SPX', 'SPY'])
    #print YahooScraper().get_current_data(['YM=F', 'ES=F'])
    print BarChartScraper().get_current_data(['XIV', 'SVXY'])
    #print MarketWatchScraper().get_current_data(['DJI', 'SPX'])
