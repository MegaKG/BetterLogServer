#!/usr/bin/env python3
import time
import mysql.connector as mc
import hashlib
import lib.logParser as logParser


def sha256(IN):
 return hashlib.sha256(IN).hexdigest()


class saver:
    def __init__(self, handlers, statisticEngines, hashBuffer=1000):
        self.handlers = handlers
        self.lastHashes = {}

        self.hashBuffer = hashBuffer
        
        self.statistics_totalCount = {}
        self.statisticEngines = statisticEngines

        for handlerName in handlers:
           self.statistics_totalCount[handlerName] = 0

        for engine in self.statisticEngines:
           engine.addStatistic(self.statistics_totalCount)
           engine.run()



    def log(self,data):
        try:
            parsed = logParser.parse(data)

            hsh = sha256(parsed['message'])
            if hsh in self.lastHashes.values():
             #print("Block",parsed['message'])
             return
            
            if len(self.lastHashes) < self.hashBuffer:
                self.lastHashes[time.time()] = hsh
            else:
                del self.lastHashes[min(self.lastHashes.keys())]
                self.lastHashes[time.time()] = hsh
               

            #Send the message to the identifiers
            Stamp = parsed['stamp']

            #Find the Start of the Message
            counter = 0
            for ch in data:
                counter += 1
                if ch == ord('>'):
                    break

            #print("MSG",parsed['message'],'DATA',data)

            for handlerName in self.handlers:
                if self.handlers[handlerName]['Identifier'].assessLog(data[counter:],parsed['priority']):
                    self.handlers[handlerName]['Engine'].saveLog(data[counter:],Stamp,parsed['priority'])
                    self.statistics_totalCount[handlerName] += 1
            

        except Exception as E:
            print("Saver Error",E)
            

        

