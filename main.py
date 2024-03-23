import time
from ibapi.client import EClient
from ibapi.common import TickerId
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import random


# class for Interactive brokers connection


class IbConn(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Listening for realtime bars
    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        try:
            bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)
        except Exception as e:
            print(e)

    def error(self, id , error, error_code):
        print(id)
        print(error)
        print(error_code)


class Bot:
    ib = None

    # Connect to IB
    def __init__(self):
        client_id = random.randint(234,234234)
        self.ib = IbConn()
        self.ib.connect("127.0.0.1", 7497, clientId=client_id)
        # separate run method to separate thread
        ib_thread = threading.Thread(target=self.bot_loop(), daemon=True)
        ib_thread.start()
        time.sleep(1)
        symbol = input("Enter the symbol you want to trade: ")
        # Creating IB Contract Objects
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # Request real-time market data
        self.ib.reqRealTimeBars(0, contract, 5, "TRADES", True, [])

        #create order object
        order = Order()
        order.orderType = "MKT"
        order.action = "SELL"
        quantity = 1
        order.totalQuantity = quantity

        #create Contract object
        contract = Contract()
        contract.symbol = symbol
        contract.exchange = "SMART"
        contract.secType = "CASH" #forex
        contract.primaryExchange = "ISLAND"
        contract.currency = "USD"

        #Place the order
        order_id = random.randint(0,9000)
        self.ib.placeOrder(order_id, contract, order)




    # separate run method to separate thread
    def bot_loop(self):
        self.ib.run()

    # Pass realtime bar data to bot objects
    @staticmethod
    def on_bar_update(reqId, time, open_, high, low, close, volume, wap, count):
        print(reqId)


bot = Bot()
