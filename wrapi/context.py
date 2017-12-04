from ibbasic.api import API


class Context(object):

    def __init__(self):
        self._portfolio = None

    @property
    def portfolio(self):
        if self._portfolio is None:
            self._portfolio = API().get_portfolio_info()
        return self._portfolio



