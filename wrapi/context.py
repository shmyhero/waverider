from ibbasic.api import API
from wrapi.strategy_config import StrategyConfig


class Context(object):

    def __init__(self):
        self.strategy_name = None
        self._portfolio = None
        self.terminate_p = False

    @property
    def portfolio(self):
        if self._portfolio is None:
            self._portfolio = API().get_portfolio_info()
        return self._portfolio

    def display_all(self):
        # positions = '\r\n'.join(self.portfolio.positions_amounts)
        positions = '\n\r'
        for k,v in self.portfolio.positions_amounts:
            positions = positions + k + ':\t'+ str(v) + '\n\r'

        content = ['portfolio value:%s' % self.portfolio.portfolio_value,
                   'position value: %s' % self.portfolio.positions_value,
                   'capital used: %s' % self.portfolio.capital_used,
                   'positions amounts: %s' % positions]
        return '\r\n'.join(content)

    def get(self, section_name, key):
        return StrategyConfig(self.strategy_name).get(section_name, key)

    def set(self, section_name, key, value):
        return StrategyConfig(self.strategy_name).set(section_name, key, value)

    def terminate(self):
        self.terminate_p = True

if __name__ == '__main__':
    print Context().display_all() 

