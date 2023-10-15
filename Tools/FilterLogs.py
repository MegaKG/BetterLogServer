#!/usr/bin/env python3
import gzip
import multiprocessing
import os
import sys
import time




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

        

def isIn(ToCheck, Term):
    for c in range(len(ToCheck)):
        Matched = 0
        for a in range(len(Term)):
            if (c+a) < len(ToCheck):
                if Term[a] != ToCheck[c+a]:
                    break
                else:
                    Matched += 1
            else:
                break
        if Matched == len(Term):
            return True
    return False
                


            
    

def processFile(FileName):
 try:
    TC = timeCounter()
    
    f = gzip.open(FileName,'rb')
    g = gzip.open(FileName + '.new','wb')
    TERM = sys.argv[2].encode('utf-8')

    while True:
        l = f.readline()
        if l == b'':
            break
        else:
            TC.update("Scan Line")

            if not isIn(l, TERM):
                g.write(l)




    f.close()
    g.close()
    os.remove(FileName)
    os.rename(FileName + '.new', FileName)
    print("Done",FileName)
 except:
  pass
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

