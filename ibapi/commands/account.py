from time import sleep
from ib.opt import ibConnection, message


def my_account_handler(msg):
    print(msg)


def contract_handler(msg):
    print 'contract_obj:%s'%msg.contract.__dict__


con = ibConnection()

con.registerAll(my_account_handler)
con.register(contract_handler, 'UpdatePortfolio')
con.connect()
con.reqAccountUpdates(1, '')

sleep(1)
con.disconnect()