#!/usr/bin/env python3
import gzip
import multiprocessing
import os
import sys
import time


def numericScore(Line):
    MonthLookup = {
        'Jan':1,
        'Feb':2,
        'Mar':3,
        'Apr':4,
        'May':5,
        'Jun':6,
        'Jul':7,
        'Aug':8,
        'Sep':9,
        'Oct':10,
        'Nov':11,
        'Dec':12
        }
    while b'  ' in Line:
        Line = Line.replace(b'  ',b' ')
        
    SP = Line.split(b' ')

    Month = MonthLookup[SP[0].decode('utf-8')]
    Day = int(SP[1].decode('utf-8'))
    
    Time = SP[2].decode('utf-8')
    TSP = Time.split(':')
    
    Hour = int(TSP[0])
    Minute = int(TSP[1])
    Second = int(TSP[2])

    Stamp = (
        1e0 * Second + 
        1e2 * Minute + 
        1e4 * Hour + 
        1e6 * Day +
        1e8 * Month
        )
    return Stamp

class cacheValue:
    def __init__(self,Value):
        self.Value = Value
        self.Hits = 0

    def fetch(self):
        self.Hits += 1
        return self.Value

    def getHits(self):
        return self.Hits

    def decrScore(self):
        self.Hits -= 1


class accessCache:
    def __init__(self,cacheSize=10000):
        self.cache = {}
        self.keycount = 0
        self.minSize = cacheSize//10
        self.maxSize = cacheSize

    def searchCache(self,Key):
        if Key in self.cache:
            #print("Hit",Key)
            return self.cache[Key].fetch()
        else:
            #print("Miss",Key)
            return None

    def cleanCache(self):
        for Key in self.cache:
                self.cache[Key].decrScore()

        while len(self.cache) > self.minSize:
            #Cull the lowest hit record
            LowestKey = list(self.cache.keys())[0]
            
                
            for Key in self.cache:
                if self.cache[Key].getHits() < self.cache[LowestKey].getHits():
                    LowestKey = Key

            del self.cache[LowestKey]
                

    def insertCache(self,Key, Value):
        if self.keycount > self.maxSize:
            self.cleanCache()
        self.cache[Key] = cacheValue(Value)
                

class timeCounter:
    def __init__(self,interval=1):
        self.start = time.time()
        self.interval = interval
        self.counters = {}
        self.starts = {}
        self.ends = {}

    def update(self,Action="Default"):
        if Action in self.counters:
            self.counters[Action] += 1
        else:
            self.counters[Action] = 1

        now = time.time()
        if now - self.start > self.interval:
          try:
            Str = ''
            for Action in self.counters:
                Str += Action + ': ' + str(self.counters[Action]/(now-self.start)) + ' (' + str((self.counters[Action]/sum(self.counters.values())) * 100) + '%' + ') ' 
            print("Status: ",Str)

            Str = ''
            for Action in self.starts:
                Str += Action + ': ' + str(self.ends[Action] - self.starts[Action]) + ' (' + str(100*((self.ends[Action] - self.starts[Action])/(max(self.ends.values()) - min(self.starts.values())))) + '%) '
            print("Timing: " + Str)
          except:
            pass
            
          self.start = now
          self.counters = {}
          self.starts = {}
          self.ends = {}

    def startAction(self,Action="Default"):
       self.starts[Action] = time.time()


    def stopAction(self,Action="Default"):
       self.ends[Action] = time.time()
       self.update(Action)

        

            
    

def processFile(FileName):
    TC = timeCounter()
    
    f = gzip.open(FileName,'rb')

    LineArray = []

    #Read the positions of the start of every line
    
    while True:
        TC.startAction("IRead")
        LineArray.append(f.tell())
        if f.readline() == b'':
            break
        TC.stopAction("IRead")

    f.seek(0)

    #Create the cache
    MyCache = accessCache(100000)

    def readIndex(Index):
        nonlocal TC
        nonlocal MyCache

        TC.startAction("Query")
        QueryResult = MyCache.searchCache(Index)
        TC.stopAction("Query")
        
        
        if QueryResult is None:
            try:
                TC.startAction("FRead")
                f.seek(Index)
                line = f.readline()
                Score = numericScore(line)
                TC.stopAction("FRead")

                TC.startAction("Insert")
                MyCache.insertCache(Index,Score)
                TC.stopAction("Insert")
                return Score
            except Exception as E:
                return -1
        else:
            return QueryResult

    print("Read File Positions",FileName)

    #Here we do a quicksort
    g = gzip.open(FileName + '.tmp','wb')

    
    
    def quickSort(Array):
        #print("Array",len(Array))
        nonlocal TC
        if len(Array) <= 1:
            return Array
        
        Pivot = readIndex(Array[int(len(Array)/2)])
        if Pivot > 0:
        
            LowBucket = []
            HighBucket = []
            SameBucket = []

            for element in Array:
                value = readIndex(element)
                if value < Pivot:
                    LowBucket.append(element)
                elif value > Pivot:
                    HighBucket.append(element)
                elif value == Pivot:
                    SameBucket.append(element)

            return quickSort(LowBucket) + SameBucket + quickSort(HighBucket)
        return []

    #TC.startAction("Sort")
    SortedIndexes = quickSort(LineArray)
    #TC.stopAction("Sort")
    print("Sorted The Indexes",FileName)

    for key in SortedIndexes:
        TC.startAction("Copy")
        f.seek(key)
        Line = f.readline()
        g.write(Line)
        TC.startAction("Copy")

    print("Done",FileName)

    f.close()
    g.close()

    #Copy the File
    os.remove(FileName)
    os.rename(FileName + '.tmp', FileName)
    print("Renamed",FileName)

if __name__ == '__main__':
    cpu_count = multiprocessing.cpu_count()
    print("System has",cpu_count,"CPUs")

    def recurse(IN):
        files = os.listdir(IN)
        Out = []
        for i in files:
            v = IN + '/' + i
            if os.path.isdir(v):
                Out += recurse(v)
            else:
                if '.gz' in i:
                    print("Find",v)
                    Out.append(v)
        return Out

    Files = recurse(sys.argv[1])

    pool = multiprocessing.Pool(cpu_count)
    pool.map(processFile,Files)

