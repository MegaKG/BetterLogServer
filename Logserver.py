#!/usr/bin/env python3
from http import client
import SendMail3 as sm
import TCPstreams5 as tcp
import UDPstreams3 as udp
import threading
import time
import logvalidity as lv
import logsaver


class slidingInput:
    def __init__(self,denoteby,maxbuf):
        self.denoteby = denoteby
        self.buffer = []
        self.maxbuf = maxbuf
    
    def add(self,data):
        for i in data:
            self.buffer.append(i)

    def getavailable(self):
        Out = []

        temp = bytearray()
        wordl = 0
        lastend = 0
        for count in range(len(self.buffer)):
            if (self.buffer[count] == self.denoteby) or (wordl == self.maxbuf):
                Out.append(bytes(temp))
                temp.clear()
                wordl = 0
                lastend = count
            else:
                wordl += 1
                temp.append(self.buffer[count])

        self.buffer = self.buffer[lastend:]
        return Out
            


        

class logserver:
    def __init__(self,Args):
        self.config = Args
        self.threads = []
        self.Run = True
        self.idcounter = 0
        self.saver = logsaver.saver(Args)
        self.lock = False

    def injestlog(self,log):
        #print(log)
        #Now we check the logs
        if not lv.check(log):
            print("REJECT",log)
            return
    
        #Now log it
        while self.lock:
         time.sleep(0.1)
        self.lock = True
        self.saver.log(log)
        self.lock = False



    def client(self,Connection,ID):
        print("Connection Init",ID)
        SL = slidingInput(b'\n'[0],self.config['maxlen'])
        while True:
            data = Connection.getdat(1024)
            print("IN",data)
            if (data == b'') or (data == False):
                break
            else:
                SL.add(data)

                Lines = SL.getavailable()
                for i in Lines:
                    print(i)
                    self.injestlog(i)
        print("Connection Died",ID)


    def tcpserver(self):
        server = tcp.newServer(self.config['host'],self.config['port'])

        while True:
            con = tcp.serverCon(server)
            print("TCP Client")
            clientthread = threading.Thread(target=self.client,args=(con,self.idcounter),name='TCP Log Client Connection')
            clientthread.start()
            self.threads.append(clientthread)
            self.idcounter += 1

    def udpserver(self):
        server = udp.newServer(self.config['host'],self.config['port'])

        while True:
            con = udp.serverCon(server)
            print("UDP Client")
            clientthread = threading.Thread(target=self.client,args=(con,self.idcounter),name='UDP Log Client Connection')
            clientthread.start()
            self.threads.append(clientthread)
            self.idcounter += 1

    def run(self):
        if self.config['tcp']:
            print("Starting TCP Server")
            tcpthread = threading.Thread(target=self.tcpserver,name="TCP Log Server")
            tcpthread.start()
            self.threads.append(tcpthread)

        if self.config['udp']:
            print("Starting UDP Server")
            udpthread = threading.Thread(target=self.udpserver,name="UDP Log Server")
            udpthread.start()
            self.threads.append(udpthread)


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



if __name__ == '__main__':
    import Config
    server = logserver(Config.LaunchArgs)
    server.run()
