from ibbasic.api import API


class Context(object):

    def __init__(self):
        self._portfolio = None

    @property
    def portfolio(self):
        if self._portfolio is None:
            self._portfolio = API().get_portfolio_info()
        return self._portfolio

    def display_all(self):
        content = ['portfolio value:%s' % self.portfolio.portfolio_value,
                   'position value: %s' % self.portfolio.positions_value,
                   'capital used: %s' % self.portfolio.capital_used,
                   'positions amounts: %s' % self.portfolio.positions_amounts]
        return '\r\n'.join(content)


if __name__ == '__main__':
    print Context().display_all() 

