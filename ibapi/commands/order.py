import sys
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message

def error_handler(msg):
    """Handles the capturing of error messages"""
    print "Server Error: %s" % msg

def reply_handler(msg):
    """Handles of server replies"""
    print "Server Response: %s, %s" % (msg.typeName, msg)


def create_contract(symbol, sec_type, exch, prim_exch, curr):
    """Create a Contract object defining what will
    be purchased, at which exchange and in which currency.

    symbol - The ticker symbol for the contract
    sec_type - The security type for the contract ('STK' is 'stock')
    exch - The exchange to carry out the contract on
    prim_exch - The primary exchange to carry out the contract on
    curr - The currency in which to purchase the contract"""
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract


def create_order(order_type, quantity, action, price = None):
    """Create an Order object (Market/Limit) to go long/short.

    order_type - 'MKT', 'LMT' for Market or Limit orders
    quantity - Integral number of assets to order
    action - 'BUY' or 'SELL'"""
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    if order_type == 'LMT':
        order.m_lmtPrice = price
    elif order_type == 'STP':
        order.m_auxPrice = price
    return order


def main(order_id, symbol, sec_type, order_type, quantity, action, price = None):

    # Connect to the Trader Workstation (TWS) running on the
    # usual port of 7496, with a clientId of 100
    # (The clientId is chosen by us and we will need
    # separate IDs for both the execution connection and
    # market data connection)
    tws_conn = Connection.create(port=7496, clientId=100)
    tws_conn.connect()

    # Assign the error handling function defined above
    # to the TWS connection
    tws_conn.register(error_handler, 'Error')

    # Assign all of the server reply messages to the
    # reply_handler function defined above
    tws_conn.registerAll(reply_handler)

    contract = create_contract(symbol, sec_type, 'SMART', 'SMART', 'USD')

    # Go long 100 shares of Google
    order = create_order(order_type, quantity, action, price)

    # Use the connection to the send the order to IB
    tws_conn.placeOrder(order_id, contract, order)

    # Disconnect from TWS
    tws_conn.disconnect()


if __name__ == "__main__":
    order_id = int(sys.argv[1])
    symbol = sys.argv[2]
    sec_type = sys.argv[3]
    order_type = sys.argv[4]
    quantity = int(sys.argv[5])
    action = sys.argv[6]
    price = None
    if len(sys.argv) > 7 and sys.argv[7] != '':
        try:
            price = float(sys.argv[7])
        except Exception:
            pass

    main(order_id, symbol, sec_type, order_type, quantity, action, price)

