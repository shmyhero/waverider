from time import sleep
from ib.opt import ibConnection, message


def msg_handler(msg):
    print(msg)


def order_handler(msg):
    print 'order_obj:%s' % msg.order.__dict__


def contract_handler(msg):
    print 'contract_obj:%s' % msg.contract.__dict__

con = ibConnection()
con.registerAll(msg_handler)
con.register(order_handler, 'OpenOrder')
con.register(contract_handler, 'OpenOrder')
con.connect()
con.reqAllOpenOrders()
sleep(3)
con.disconnect()