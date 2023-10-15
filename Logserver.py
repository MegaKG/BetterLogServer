#!/usr/bin/env python3
import lib.TCPstreams5 as tcp
import lib.UDPstreams3 as udp
import lib.logvalidity as logValid
import lib.logsaver as logSave
import lib.slidingInput as slideInput

import threading
import time
            


        

class logserver:
    def __init__(self,hostIP,hostPort,handlers={},statistics=[],tcpEnable=True,udpEnable=True,maxLogLength=1024,maxThreadCount=128,deduplicatorLength=1000,designator="Default"):
        self.hostIP = hostIP
        self.hostPort = hostPort
        self.handlers = handlers

        self.enableTCP = tcpEnable
        self.enableUDP = udpEnable

        self.maxLen = maxLogLength
        self.maxClients = maxThreadCount

        self.statistics = statistics

        self.des = designator

        self.threads = []
        self.threadFlags = []
        self.Run = True
        self.idcounter = 0

        self.lock = False

        self.deduplicatorLength = deduplicatorLength

        self.saver = logSave.saver(handlers,statistics,self.deduplicatorLength)
        

    def injestlog(self,log):
        #print(log)
        #Now we check the logs
        if not logValid.check(log):
            #print(self.des,"REJECT",log)
            return
    
        #Now log it
        while self.lock:
         time.sleep(0.1)
        self.lock = True

        try:
         self.saver.log(log)
        except Exception as E:
         print(self.des,"Fatal: Main Saver Broke, Reinitialising")
         del self.saver
         self.saver = logSave.saver(self.handlers,self.statistics,self.deduplicatorLength)

        self.lock = False



    def client(self,Connection,ID):
        print(self.des,"Connection Init",ID)
        SLparser = slideInput.slidingInput(ord('\n'),self.maxLen)

        while True:
            data = Connection.getdat(1024)
            #print("IN",data)
            if (data == b'') or (data == False):
                break
            else:
                SLparser.add(data)

                Lines = SLparser.getavailable()
                for i in Lines:
                    #print(i)
                    self.injestlog(i)
        print(self.des,"Connection Died",ID)


    def tcpServer(self):
        server = tcp.newServer(self.hostIP,self.hostPort)

        while True:
            while len(self.threads) > self.maxClients:
                time.sleep(0.1)

            con = tcp.serverCon(server)
            print(self.des,"TCP Client")
            clientthread = threading.Thread(target=self.client,args=(con,self.idcounter),name='TCP Log Client Connection')
            clientthread.start()
            self.threads.append(clientthread)
            self.threadFlags.append(1)
            self.idcounter += 1

    def udpServer(self):
        server = udp.newServer(self.hostIP,self.hostPort)

        while True:
            while len(self.threads) > self.maxClients:
                time.sleep(0.1)

            con = udp.serverCon(server)
            print(self.des,"UDP Client")
            clientthread = threading.Thread(target=self.client,args=(con,self.idcounter),name='UDP Log Client Connection')
            clientthread.start()
            self.threads.append(clientthread)
            self.threadFlags.append(1)
            self.idcounter += 1

    def run(self):
        if self.enableTCP:
            print(self.des,"Starting TCP Server")
            tcpthread = threading.Thread(target=self.tcpServer,name="TCP Log Server")
            tcpthread.start()
            self.threads.append(tcpthread)
            self.threadFlags.append(1)

        if self.enableUDP:
            print(self.des,"Starting UDP Server")
            udpthread = threading.Thread(target=self.udpServer,name="UDP Log Server")
            udpthread.start()
            self.threads.append(udpthread)
            self.threadFlags.append(1)


        ToKill = set()
        while self.Run:
            time.sleep(60)

            #Kill Old Threads
            ToKill.clear()
            for i in self.threads:
                if not i.is_alive():
                    ToKill.add(i)

            for i in ToKill:
                self.threads.remove(i)

class main:
    def __init__(self,config):
        self.config = config
        self.serverThreads = []

    def runServer(self,serverConfig,serverID):
        Server = logserver(
                serverConfig['host'],
                serverConfig['port'],
                serverConfig['Handlers'],
                serverConfig['Statistics'],
                serverConfig['tcp'],
                serverConfig['udp'],
                serverConfig['maxLen'],
                serverConfig['maxThreads'],
                serverConfig['deduplicateQueue'],
                serverID
                )
        Server.run()


    def run(self):
        for serverConfigID in self.config['servers']:
            serverConfig = self.config['servers'][serverConfigID]
            print("Initialising Server",serverConfigID)

            t = threading.Thread(target=self.runServer,args=(serverConfig,serverConfigID),name=serverConfigID)
            t.start()
            self.serverThreads.append(t)

        while (True):
            time.sleep(1)





if __name__ == '__main__':
    import Config
    app = main(Config.LaunchArgs)
    app.run()
