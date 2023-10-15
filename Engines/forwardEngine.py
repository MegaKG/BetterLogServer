import lib.TCPstreams5 as tcp
import lib.UDPstreams3 as udp
import time

class saver:
    def reconnect(self,init=False):
       if init:
         self.lastConnect = True

       if (time.time() - self.lastConnect > 60) or init:
        self.lastConnect = time.time()
        try:
         if self.mode:
            self.CON = udp.clientCon(self.serverIP,self.serverPort)
         else:
            self.CON = tcp.clientCon(self.serverIP,self.serverPort)
         print("Uplink Success",self.serverIP,self.serverPort)
        except Exception as E:
         print("Uplink Connection Error",E)


    def __init__(self,serverIP,serverPort=514,udpMode=False):
        self.serverIP = serverIP
        self.serverPort = serverPort

        self.mode = udpMode

        self.CON = None
        self.reconnect(True)


    def saveLog(self,Log,MessageStamp,Faculty):
        try:
            self.CON.senddat(b'<' + str(Faculty).encode() + b'>' + Log + b'\n')
        except Exception as E:
            #print("Forward Disconnect")
            self.reconnect()
#            self.saveLog(Log,MessageStamp,Faculty)
