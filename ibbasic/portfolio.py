
class Position(object):

    def __init__(self, symbol, quantity, market_price, cost_price):
        self.symbol = symbol
        self.amount = quantity
        self.last_sale_price = market_price
        self.cost_basic = cost_price

    @property
    def value(self):
        return self.amount * self.last_sale_price

    @property
    def cost(self):
        return self.amount * self.cost_basic


class Portfolio(object):

    def __init__(self, available_funds, net_liquidation, contact_dict):
        self.available_funds = available_funds
        self.net_liquidation = net_liquidation
        self.contract_dict = contact_dict
        self.positions = self.init_positions()

    def init_positions(self):
        positions = {}
        for (symbol, (quantity, market_price, cost_price)) in self.contract_dict.items():
            positions[symbol] = Position(symbol, quantity, market_price, cost_price)
        return positions

    def get_quantity(self, symbol):
        if self.contract_dict.has_key(symbol):
            return self.contract_dict[symbol][0]
        else:
            return 0

    def get_percentage(self, symbol):
        if self.contract_dict.has_key(symbol):
            (quantity, market_price, cost_price) = self.contract_dict[symbol]
            return quantity * market_price / self.net_liquidation
        else:
            return 0

    @property
    def portfolio_value(self):
        return self.net_liquidation

    @property
    def positions_value(self):
        return sum(map(lambda x: x.value, self.positions.values()))

    @property
    def capital_used(self):
        return sum(map(lambda x: x.cost, self.positions.values()))


def __str__(self):
        return str(self.__dict__)



