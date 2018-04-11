from backtest.portfolio import Portfolio, Position


class API(object):

    def __init__(self, data, init_funds=100000):
        self.data = data
        self.portfolio = Portfolio(init_funds)

    def get_portfolio_info(self):
        return self.portfolio

    def get_market_value(self):
        total = self.portfolio.available_funds
        for [symbol, amount] in self.portfolio.positions_amounts:
            total += self.data.current(symbol) * amount
        return total

    def order(self, symbol, quantity):
        if quantity != 0:
            try:
                price = self.data.current(symbol)
            except:
                price = self.data.history(symbol, window=1)[0]
            exist_amount = self.portfolio.positions[symbol].amount
            self.portfolio.positions[symbol] = Position(symbol, exist_amount + quantity, 0, 0)
            self.portfolio.available_funds -= quantity * price




