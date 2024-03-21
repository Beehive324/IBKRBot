from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import ibapi

# class for Interactive brokers connection


class IbConn(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)


class Bot:
    ib = None
    #Connect to IB

    def __init__(self):
        ib = IbConn()
        ib.connect("127.0.0.1", 7497,2)
        ib.run()


bot = Bot()
