#!/usr/bin/env python3
import threading
import Engines.UNIXstreams4 as UNIXstreams4

class saver:
    def serverAcceptor(self):
        while True:
            for i in reversed(self.clientCons):
                if not i.isAlive():
                    self.clientCons.remove(i) 

            CON = UNIXstreams4.serverCon(self.Server)
            print("Accepted Remote View Client")
            self.clientCons.append(CON)


    def __init__(self,path = '/run/logserver'):
        self.path = path

        self.clientCons = []

        self.Server = UNIXstreams4.newServer(path)
        self.acceptor = threading.Thread(target=self.serverAcceptor)
        self.acceptor.start()

    def saveLog(self,Log,MessageStamp,Faculty):
        for con in self.clientCons:
            con.senddat(Log + b'\n')