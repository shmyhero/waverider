#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep


# print all messages from TWS
def watcher(msg):
    print msg


# print out all ticket price
def ticket_price_handler(msg):
    print msg


def get_market_value(symbol, sec_type, exchange, currency, expiry, strike, right):
    con = ibConnection()
    con.registerAll(watcher)
    showBidAskOnly = True  # set False to see the raw messages
    if showBidAskOnly:
        con.unregister(watcher, message.tickSize, message.tickPrice,
                       message.tickString, message.tickOptionComputation)
        con.register(ticket_price_handler, message.tickPrice)
    con.connect()
    sleep(1)
    tickId = 1
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exchange
    contract.m_currency = currency
    contract.m_expiry = expiry
    contract.m_strike = strike
    contract.m_right = right
    print ('* * * * REQUESTING MARKET DATA * * * *')
    con.reqMktData(tickId, contract, '', False)
    sleep(2)
    print ('* * * * CANCELING MARKET DATA * * * *')
    con.cancelMktData(tickId)
    sleep(1)
    con.disconnect()


def get_argv(index, defualt_value = ''):
    if len(sys.argv)> index:
        return sys.argv[index]
    else:
        return defualt_value


# argv order: symbol, sec_type, exchange, currency, strike, expiry, right
def main():
    get_market_value(get_argv(1), get_argv(2), get_argv(3), get_argv(4), get_argv(6), float(get_argv(5)), get_argv(7))


if __name__ == '__main__':
    # sys.argv = ['', 'SPY', 'STK', 'SMART', 'USD', 0.0, '', '']
    # sys.argv = ['', 'SPY', 'OPT', 'SMART', 'USD', 258.0, '20171215', 'CALL']
    main()
