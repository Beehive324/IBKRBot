import time
from ibapi.client import EClient
from ibapi.common import TickerId
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading


# class for Interactive brokers connection


class IbConn(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Listening for realtime bars
    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)


class Bot:
    ib = None

    # Connect to IB

    def __init__(self):
        self.ib = IbConn()
        self.ib.connect("127.0.0.1", 7497, 2)
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

    # separate run method to separate thread
    def bot_loop(self):
        self.ib.run()

    # Pass realtime bar data to bot objects
    @staticmethod
    def on_bar_update(reqId, time, open_, high, low, close, volume, wap, count):
        print(reqId)


bot = Bot()
