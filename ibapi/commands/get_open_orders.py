from time import sleep
from ib.opt import ibConnection, message

con = ibConnection()
con.connect()
con.reqAllOpenOrders()
sleep(2)
con.disconnect()