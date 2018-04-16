from collections import MutableMapping


class Position(object):

    def __init__(self, symbol, quantity):
        self.symbol = symbol
        self.amount = quantity

    def __str__(self):
        return str(self.__dict__)


class Positions(MutableMapping):

    def __init__(self, *args, **kw):
        self._storage = dict(*args, **kw)

    def __getitem__(self, key):
        if key in self._storage.keys():
            return self._storage[key]
        else:
            return Position(key, 0)

    def __setitem__(self, key, value):
        self._storage[key] = value

    def __delitem__(self, key):
        self._storage.pop(key)

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)


class Portfolio(object):

    def __init__(self, init_funds):
        self.available_funds = init_funds
        self.positions = Positions()

    def get_quantity(self, symbol):
        return self.positions[symbol].amount

    @property
    def positions_amounts(self):
        return filter(lambda x: x[1] != 0, map(lambda x: [x.symbol, x.amount], self.positions.values()))

    def get_positions_value(self, data, daily_price=False):
        total = 0
        for [symbol, amount] in self.positions_amounts:
            if daily_price:
                total += data.get_daily_price(symbol) * amount
            else:
                total += data.get_market_price(symbol) * amount
        return total

    def get_portfolio_value(self, data, daily_price=False):
        return self.get_positions_value(data, daily_price) + self.available_funds

    def get_percentage(self, symbol, data):
        if symbol in self.positions.keys():
            quantity = self.get_quantity(symbol)
            return quantity * data.get_market_price(symbol) / self.get_portfolio_value(data)
        else:
            return 0

    @property
    def capital_used(self):
        # return sum(map(lambda x: x.cost, self.positions.values()))
        pass

    def to_dict(self):
        dic = {}
        for key in self.__dict__.keys():
            if key != 'positions':
                dic[key] = self.__dict__[key]
        return dic

    @staticmethod
    def from_dict(dic):
        return Portfolio(dic['available_funds'], dic['net_liquidation'], dic['contract_dict'])

