from collections import MutableMapping


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

    def __str__(self):
        return str(self.__dict__)


class Positions(MutableMapping):

    def __init__(self, *args, **kw):
        self._storage = dict(*args, **kw)

    def __getitem__(self, key):
        if key in self._storage.keys():
            return self._storage[key]
        else:
            return 0

    def __setitem__(self, key, value):
        self._storage[key] = value

    def __delitem__(self, key):
        self._storage.pop(key)

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)


class Portfolio(object):

    def __init__(self, available_funds, net_liquidation, contact_dict):
        self.available_funds = available_funds
        self.net_liquidation = net_liquidation
        self.contract_dict = contact_dict
        self.positions = self.init_positions()

    def init_positions(self):
        positions = Positions()
        for (symbol, (quantity, market_price, cost_price)) in self.contract_dict.items():
            if quantity != 0:
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
    def positions_amounts(self):
        return map(lambda x: [x.symbol, x.amount], self.positions.values())

    @property
    def capital_used(self):
        return sum(map(lambda x: x.cost, self.positions.values()))

    def to_dict(self):
        dic = {}
        for key in self.__dict__.keys():
            if key != 'positions':
                dic[key] = self.__dict__[key]
        return dic

    @staticmethod
    def from_dict(dic):
        return Portfolio(dic['available_funds'], dic['net_liquidation'], dic['contract_dict'])

