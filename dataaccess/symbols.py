
class Symbols(object):

    YahooSymbolMapping = {'SPX': '^GSPC', 'INDU': '^DJI', 'DJI': '^DJI', 'VIX': '^VIX', 'VXV': '^VXV', 'VVIX': '^VVIX', 'RUT': '^RUT', 'NDX': '^NDX', 'VXMT': '^VXMT'}

    Indexes = ['SPX', 'INDU', 'VIX', 'VXV', 'VVIX', 'RUT', 'NDX', 'VXMT']

    @staticmethod
    def get_mapped_symbol(symbol, mapping_dic=YahooSymbolMapping):
        if symbol in mapping_dic.keys():
            return mapping_dic[symbol]
        else:
            return symbol
