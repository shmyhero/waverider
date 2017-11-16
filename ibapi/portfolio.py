
class Portfolio(object):

    def __init__(self, total_cash, net_liquidation, contact_dict):
        self.total_cash = total_cash
        self.net_liquidation = net_liquidation
        self.contract_dict = contact_dict

    def get_quantity(self, symbol):
        if self.contract_dict.has_key(symbol):
            return self.contract_dict[symbol][0]
        else:
            return 0

    def get_percentage(self, symbol):
        if self.contract_dict.has_key(symbol):
            (quantity, price) = self.contract_dict[symbol]
            return quantity * price / self.net_liquidation
        else:
            return 0

    def __str__(self):
        return str(self.__dict__)



