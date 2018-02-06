import sys
import time
from ib.opt import Connection
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from common.configmgr import ConfigMgr


def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg


def reply_handler(msg):
    """Handles of server replies"""
    print "Server Response: %s, %s" % (msg.typeName, msg)


def main(order_id):

    # Connect to the Trader Workstation (TWS) running on the
    # usual port of 7496, with a clientId of 100
    # (The clientId is chosen by us and we will need
    # separate IDs for both the execution connection and
    # market data connection)
    tws_conn = Connection.create(port=7496, clientId=int(ConfigMgr.get_ib_config()['order_client_id']))
    tws_conn.connect()

    # Assign the error handling function defined above
    # to the TWS connection
    tws_conn.register(error_handler, 'Error')

    # Assign all of the server reply messages to the
    # reply_handler function defined above
    tws_conn.registerAll(reply_handler)

    tws_conn.cancelOrder(order_id)

    time.sleep(3)

    # Disconnect from TWS
    tws_conn.disconnect()


if __name__ == "__main__":
    # sys.argv = ['', '100014']
    order_id = int(sys.argv[1])
    main(order_id)

