#!/usr/bin/env python3
import threading
import UNIXstreams4

class saver:
    def serverAcceptor(self):
        while True:
            for i in reversed(self.clientCons):
                if not i.isAlive():
                    self.clientCons.remove(i) 

            CON = UNIXstreams4.serverCon(self.Server)
            print("Accepted Remote View Client")
            self.clientCons.append(CON)


    def __init__(self,Config,filename = '/run/logserver'):
        self.filename = filename
        self.Config = Config

        self.clientCons = []

        self.Server = UNIXstreams4.newServer(filename)
        self.acceptor = threading.Thread(target=self.serverAcceptor)
        self.acceptor.start()

    def saveLog(self,Log,MessageStamp):
        for con in self.clientCons:
            con.senddat(Log + b'\n')