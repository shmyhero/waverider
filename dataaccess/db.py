import traceback
import datetime
import mysql.connector
from utils.logger import DailyLoggerFactory
from common.pathmgr import PathMgr
from common.configmgr import ConfigMgr


def get_logger():
    return DailyLoggerFactory.get_logger(__name__, PathMgr.get_log_path())


class BaseDAO(object):

    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        db_config = ConfigMgr.get_db_config()
        return mysql.connector.connect(host=db_config['host'], user=db_config['user'], password=db_config['password'], database=db_config['database'])

    def select(self, query, cursor=None):
        # get_logger().info('query:%s' % query)
        conn = None
        if cursor is None:
            conn = BaseDAO.get_connection()
            cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            error_message = "Query:{}, error message: {}, Stack Trace: {}".format(query, str(e), traceback.format_exc())
            get_logger().exception(error_message)
        finally:
            if conn:
                conn.close()

    # def __init__(self):
    #     self.conn = BaseDAO.get_connection()
    #     self.cursor = self.conn.cursor()
    #
    # @staticmethod
    # def get_connection():
    #     db_config = ConfigMgr.get_db_config()
    #     return mysql.connector.connect(host=db_config['host'], user=db_config['user'], password=db_config['password'], database=db_config['database'])
    #
    # def select(self, query):
    #     if self.conn.is_connected() is False:
    #         self.conn = BaseDAO.get_connection()
    #         self.cursor = self.conn.cursor()
    #     try:
    #         self.cursor.execute(query)
    #         rows = self.cursor.fetchall()
    #         return rows
    #     except Exception as e:
    #         error_message = "Query:{}, error message: {}, Stack Trace: {}".format(query, str(e), traceback.format_exc())
    #         get_logger().exception(error_message)
    #         self.cursor.close()
    #         self.conn.close()



class YahooEquityDAO(BaseDAO):

    def __init__(self):
        BaseDAO.__init__(self)

    def get_equity_price_by_date(self, symbol, date_str, price_field = 'closePrice'):
        """
        :param symbol:
        :param date_str: the format is 'YYYY-mm-dd'
        :param price_field:
        :return: price
        """
        query_template = """select {} from yahoo_equity where symbol = '{}' and tradeDate <= str_to_date('{}', '%Y-%m-%d') order by tradeDate desc limit 1"""
        query = query_template.format(price_field, symbol, date_str)
        rows = self.select(query)
        if rows is None or len(rows) < 1:
            return None
        else:
            return rows[0][0]

    def get_equity_prices_by_start_end_date(self, symbol, start_date, end_date, price_field='adjClosePrice'):
        query_template = """select tradeDate, {} from yahoo_equity where symbol = '{}' and tradeDate >= '{}' and tradeDate<= '{}' order by tradeDate """
        query = query_template.format(price_field, symbol, start_date, end_date)
        rows = self.select(query)
        return rows

    def get_all_equity_price_by_symbol(self, symbol, from_date_str='1993-01-01', price_field = 'adjClosePrice'):
        query_template = """select tradeDate, {} from yahoo_equity where symbol = '{}' and tradeDate >= str_to_date('{}', '%Y-%m-%d') order by tradeDate"""
        query = query_template.format(price_field, symbol, from_date_str)
        rows = self.select(query)
        return rows

    def get_equity_monthly_price_by_symbol(self, symbol, from_date_str='1993-01-01', price_field = 'adjClosePrice'):
        """
        :param symbol: eg: SPY
        :return: rows
        """
        query_template = """select lastdate, {} from yahoo_equity_monthly_view where symbol = '{}'"""
        query = query_template.format(price_field, symbol)
        rows = self.select(query)
        return rows

    def get_realtime_time_and_price(self, symbol='SVXY', start_time=datetime.datetime(1971, 1, 1, 0, 0, 0), end_time=datetime.datetime(9999, 1, 1, 0, 0, 0)):
        query = """select tradeTime, price from equity_realtime where tradeTime >= '{}' and tradeTime <= '{}' and symbol = '{}' order by tradeTime """.format(start_time, end_time, symbol)
        return self.select(query)

    def get_min_time_and_price_from_realtime(self, symbol='SVXY', start_time=datetime.datetime(2018, 2, 7, 9, 30, 0), end_time=datetime.datetime(9999, 1, 1, 0, 0, 0)):
        rows = self.get_realtime_time_and_price(symbol, start_time, end_time)
        new_rows = []
        last_min = -1
        for row in rows:
            trade_time = row[0]
            if last_min != trade_time.minute:
                last_min = trade_time.minute
                new_rows.append(row)
        return new_rows

    def get_min_time_and_price_from_min(self, symbol, start_time=datetime.datetime(1971, 1, 1, 0, 0, 0), end_time=datetime.datetime(9999, 1, 1, 0, 0, 0)):
        query = """select tradeTime, closePrice from equity_min where tradeTime >= '{}' and tradeTime <= '{}' and tradeTime not like '%09:30:00' and symbol = '{}' order by tradeTime """.format(
            start_time, end_time, symbol)
        rows = self.select(query)
        return rows

    def get_min_time_and_price(self, symbol, start_time=datetime.datetime(1971, 1, 1, 0, 0, 0), end_time=datetime.datetime(9999, 1, 1, 0, 0, 0)):
        if symbol == 'SVXY' and start_time >= datetime.datetime(2018, 2, 7, 9, 30, 0):
            return self.get_min_time_and_price_from_realtime('SVXY', start_time, end_time)
        else:
            return self.get_min_time_and_price_from_min(symbol, start_time, end_time)


if __name__ == '__main__':
    print YahooEquityDAO().get_equity_prices_by_start_end_date('SPY', datetime.datetime(2018, 1, 1, 0, 0, 0), datetime.datetime(2018, 3, 1, 0, 0, 0))
    # print YahooEquityDAO().get_min_time_and_price('SPY', datetime.datetime(2018, 4, 1, 0, 0, 0), datetime.datetime(2018, 4, 3, 0, 0, 0))
