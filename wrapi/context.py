import datetime
import pytz
from ibbasic.api import API
from wrapi.strategy_config import StrategyConfig


class Context(object):

    def __init__(self):
        self.strategy_name = None
        self.terminate_p = False

    @property
    def portfolio(self):
        return API().get_portfolio_info()

    def display_all(self):
        # positions = '\r\n'.join(self.portfolio.positions_amounts)
        positions = '\n\r'
        for k, v in self.portfolio.positions_amounts:
            if len(k) > 15:
                underlying = k[0:-15]
                exp_date = datetime.datetime.strptime(k[-15:-9],'%y%m%d')
                if k[-9] == 'C':
                    call_or_put = 'Call'
                else:
                    call_or_put = 'Put'
                strike_price = float(k[-8:])/1000
                symbol = '%s, %s, %s %s' %(underlying, exp_date.strftime('%Y-%m-%d'), strike_price, call_or_put)
            else:
                symbol = k
            positions = positions + symbol + ':\t'+ str(v) + '\n\r'

        content = ['portfolio value:%s' % self.portfolio.portfolio_value,
                   'position value: %s' % self.portfolio.positions_value,
                   'capital used: %s' % self.portfolio.capital_used,
                   'positions amounts: %s' % positions]
        return '\r\n'.join(content)

    def get(self, section_name, key):
        return StrategyConfig(self.strategy_name).get(section_name, key)

    def set(self, section_name, key, value):
        return StrategyConfig(self.strategy_name).set(section_name, key, value)

    def end(self):
        self.terminate_p = True
        # raise Exception("Terminated...")

    def now(self):
        return datetime.datetime.now(tz=pytz.timezone('US/Eastern'))

    def now_tostring(self):
        return self.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    # print Context().display_all()
    print Context().now_tostring()

