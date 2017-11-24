from ibbasic.api import API


class Context(object):

    def __init__(self):
        self.portfolio = API().get_portfolio_info()



