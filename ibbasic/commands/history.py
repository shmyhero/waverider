#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep


# print all messages from TWS
def watcher(msg):
    print msg


# print out all ticket price
def ticket_price_handler(msg):
    print msg


def get_historical_data(symbol, duration_str, barsize_setting):
    con = ibConnection()
    con.registerAll(watcher)
    con.unregister(watcher, message.tickSize, message.tickPrice,
                   message.tickString, message.tickOptionComputation)
    con.register(ticket_price_handler, message.tickPrice)
    con.connect()
    sleep(1)
    tickId = 2
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = 'STK'
    contract.m_exchange = 'SMART'
    contract.m_primaryExch = 'SMART'
    contract.m_currency = 'USD'
    contract.m_localSymbol = symbol
    print ('* * * * REQUESTING Historical DATA * * * *')
    endtime = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
    con.reqHistoricalData(tickId, contract, endtime, durationStr=duration_str, barSizeSetting=barsize_setting, whatToShow='TRADES', useRTH=1, formatDate=1)
    sleep_time = 3
    if barsize_setting == '1 min':
        days = int(duration_str.split(' ')[0])
        sleep_time += days/3
    print sleep_time
    sleep(sleep_time)
    print ('* * * * CANCELING Historical DATA * * * *')
    con.cancelHistoricalData(tickId)
    sleep(0.1)
    con.disconnect()


def get_argv(index, defualt_value = ''):
    if len(sys.argv)> index:
        return sys.argv[index]
    else:
        return defualt_value


# argv order: symbol, duration, barsize
def main():
    get_historical_data(get_argv(1), '%s D'% get_argv(2), '1 %s'%get_argv(3))


if __name__ == '__main__':
    # sys.argv = ['', 'SPY', '10', 'min'] # duration can not more than 20D?
    # sys.argv = ['', 'SPY', '100', 'day']
    main()
