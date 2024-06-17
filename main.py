import time
import datetime
from ibapi.client import EClient
from ibapi.common import TickerId, BarData
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import ta #technical analysis library
import numpy
import pandas as p
import pytz
import math
import threading
import random




# class for Interactive brokers connection

order_id = 1
class IbConn(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def historicalData(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, False)
        except Exception as e:
            print(e)
    def historicalDataUpdate(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, True)
        except Exception as e:
            print(e)

    #end of historical data
    def historicalDataEnd(self, reqId, start, end):
        print(reqId)

    def nextValidId(self, nextorderId):
        global order_id
        order_id = nextorderId


    # Listening for realtime bars
    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        super().realtimeBar(reqId, time, open_, high, low, close, volume, wap, count)
        try:
            bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)
        except Exception as e:
            print(e)

class Bar:
    open = 0
    high = 0
    low = 0
    volume = 0
    close = 0
    date = ''

    def __init__(self):
        self.open = 0
        self.high = 0
        self.low = 0
        self.volume = 0
        self.close = 0
        self.date = 0


class Bot:
    ib = None
    bar_size = 1
    curr_bar = Bar()
    reqId = 1
    global order_id
    smaPeriod = 50
    symbol = ""
    initial_bartime = datetime.datetime.now()

    # Connect to IB
    def __init__(self):
        client_id = random.randint(234,234234)
        self.ib = IbConn()
        self.ib.connect("127.0.0.1", 7497, clientId=client_id)
        # separate run method to separate thread
        ib_thread = threading.Thread(target=self.bot_loop(), daemon=True)
        ib_thread.start()
        time.sleep(1)
        curr_bar = Bar()
        self.bar_size = int(input("Enter bar size in minutes"))
        self.symbol = input("Enter the symbol you want to trade: ")
        min_text = ""
        if self.bar_size > 1:
            min_text = 'mins'
        else:
            min_text = 'min'
        queryTime = datetime.datetime.now() - datetime.timedelta(days=1)
        # Creating IB Contract Objects
        contract = Contract()
        contract.symbol = self.symbol.upper()
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
