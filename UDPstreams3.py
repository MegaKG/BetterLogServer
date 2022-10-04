#!/usr/bin/env python3
#All you have to worry about is the Data,Port and IP
#Buffer has a default value
#One Way, Open Two Sockets for two way

from curses.ascii import BS
import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, SO_SNDBUF, SOL_SOCKET
import threading
import time

__author__ = 'Kaelan Grainger'
__version__ = '3.0'


def version():
    print('Version: ' + __version__ + ' By: ' + __author__)
    print('Library Name: ' + str(__name__))
    return [__author__,__version__,__name__]


class miniserver:
    def mainThread(self):
        while True:
            MSG, Addr = self.sock.recvfrom(self.bs)
            if Addr not in self.Data:
                self.NewServers.append(Addr)
                self.Data[Addr] = []

            self.Data[Addr].append(MSG)

            

    def __init__(self,sock,addr,buffsize):
        self.sock = sock
        self.addr = addr
        self.bs = buffsize
        self.Data = {}
        self.NewServers = []

        self.mt = threading.Thread(target=self.mainThread,name="Socket Wrapper")
        self.mt.start()


def newServer(IP,Port,BSIZE=1024):
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_SNDBUF,BSIZE)
    s.bind((IP,Port))
    return miniserver(s,(IP,Port),BSIZE)


class serverCon:
    def __init__(self,MS):
        self.ms = MS
        while True:
            if len(self.ms.NewServers) > 0:
                break
            time.sleep(0.1)
        
        self.Addr = self.ms.NewServers[0]
        self.ms.NewServers.remove(self.Addr)

    def getdat(self,B=None):
        while True:
            if len(self.ms.Data[self.Addr]) > 0:
                break
            time.sleep(0.1)

        Mine = self.ms.Data[self.Addr][0]
        self.ms.Data[self.Addr].remove(Mine)
        return Mine

    def getstdat(self,B=None):
        return self.getdat().decode('utf-8')


    def senddat(self,Data):
        self.ms.sock.sendto(Data,self.Addr)

    def sendstdat(self,Data):
        self.senddat(Data.encode('utf-8'))

    def close():
        pass


class clientCon:
    def __init__(self,IP,Port,BSIZE=1024):
        self.Addr = (IP,Port)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET,SO_SNDBUF, BSIZE)
        self.bs = BSIZE

    def getdat(self,B=None):
        return self.sock.recvfrom(self.bs)[0]

    def getstdat(self,B=None):
        return self.getdat().decode('utf-8')

    def senddat(self,Data):
        self.sock.sendto(Data,self.Addr)

    def sendstdat(self,Data):
        self.senddat(Data.encode('utf-8'))

    def close(self):
        self.sock.close()

    
        

        




