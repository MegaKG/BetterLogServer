#!/usr/bin/env python3
import mysql.connector as mc

import hashlib
import random
import time

class cacheResult:
    def __init__(self,Value,ttl=300):
        self.Value = Value
        self.InitTime = time.time()
        self.ttl = ttl
        self.LastTime = self.InitTime
        self.UpstreamSync = False

    def get(self):
        self.LastTime = time.time()
        return self.Value

    def isOld(self,tf):
        #Will expire if ttl reached (old), maxttl reached (refresh after init time) and not awaiting upload
        return ((time.time() - self.LastTime > tf) | (time.time() - self.InitTime > self.ttl)) & (not self.UpstreamSync)

    def set(self,Value):
        self.LastTime = time.time()
        self.UpstreamSync = True
        self.Value = Value

    def unsetSync(self):
        self.UpstreamSync = False

    def setSync(self):
        self.UpstreamSync = True

    def needSync(self):
        return self.UpstreamSync

    

class cacher:
    def __init__(self,maxttl,ttl):
        self.maxttl = maxttl
        self.ttl = ttl
        self.cache = {}

    def check(self,Key):
        if Key in self.cache:
            if self.cache[Key] != True:
                return True
        return False

    def fetch(self,Key):
        return self.cache[Key].get()

    def put(self,Key,Value):
        self.cache[Key] = cacheResult(Value,self.maxttl)

    def update(self,Key,Value):
        self.cache[Key].set(Value)

    def toggleSync(self,Key):
        if self.cache[Key].needSync():
            self.cache[Key].unsetSync()
        else:
            self.cache[Key].setSync()

    def sync(self,SyncFunction,*args,**kwargs):
        for i in self.cache:
            if self.cache[i].needSync():
                self.cache[i].unsetSync()
                SyncFunction(i,*args,**kwargs)

    def cleanCache(self):
        Keys = set(self.cache.keys())
        for i in Keys:
            if self.cache[i].isOld(self.ttl):
                del self.cache[i]



def splitter(IN):
    Allow = set(b'qwertyuiopasdfghjklzxcvbnm ')
    Tmp = ''
    for i in IN.lower():
        if i in Allow:
            Tmp += chr(i)
        else:
            Tmp += ' '
    
    Out = []
    for i in Tmp.split(' '):
        if len(i) > 3:
            Out.append(i)
    return Out

class NeuralLogger:
    def __init__(self,DBCON,TableName,lr=0.01):
        self.YWeightCache = cacher(600,120)
        self.NWeightCache = cacher(600,120)
        self.NameCache = cacher(600,120)

        self.db = DBCON
        self.cur = self.db.cursor()

        self.TableName = TableName
        self.learnrate = lr

    def _predict(self,Identity):
        YResult = 0
        NResult = 0
        for i in Identity:
            #print("FTCH2",i)
            #Fetch Y
            if self.YWeightCache.check(i):
                YWeight = self.YWeightCache.fetch(i)

            else:
                self.cur.execute('select YWeight from {} where NKey=\'{}\';'.format(self.TableName,i))
                YWeight = float(self.cur.fetchall()[0][0])
                self.YWeightCache.put(i,YWeight)

            YResult += YWeight * Identity[i]

            #Fetch N
            if self.NWeightCache.check(i):
                NWeight = self.NWeightCache.fetch(i)

            else:
                self.cur.execute('select NWeight from {} where NKey=\'{}\';'.format(self.TableName,i))
                NWeight = float(self.cur.fetchall()[0][0])
                self.NWeightCache.put(i,NWeight)

            NResult += NWeight * Identity[i]



        return (YResult,NResult)


    def _train(self,Identity,YRes,NRes):
        YResult, NResult = self._predict(Identity)

        Yerror = YRes - YResult
        Nerror = NRes - NResult

        #Apply to all active weights
        for i in Identity:
            #print("FTCH",i)
            #Fetch Y
            if self.YWeightCache.check(i):
                YWeight = self.YWeightCache.fetch(i)

            else:
                self.cur.execute('select YWeight from {} where NKey=\'{}\';'.format(self.TableName,i))
                YWeight = float(self.cur.fetchall()[0][0])
                self.YWeightCache.put(i,YWeight)

            #Fetch N
            if self.NWeightCache.check(i):
                NWeight = self.NWeightCache.fetch(i)

            else:
                self.cur.execute('select NWeight from {} where NKey=\'{}\';'.format(self.TableName,i))
                NWeight = float(self.cur.fetchall()[0][0])
                self.NWeightCache.put(i,NWeight)


            #Update the Weights
            YWeight += (Yerror * Identity[i] * self.learnrate)
            NWeight += (Nerror * Identity[i] * self.learnrate)
            
            self.YWeightCache.update(i,YWeight)
            self.NWeightCache.update(i,NWeight)
            



    def _toIdent(self,Line,Splitter=splitter,AddNew=False):
        SP = Splitter(Line)
        del Line

        Identity = {}
        for i in SP:
            HSH = hashlib.sha256(i.encode()).hexdigest()

            #Hit the Cache
            if self.NameCache.check(HSH):
                #print("HitCache",HSH)
                Exist = self.NameCache.fetch(HSH)
                #print("Hitval",Exist)

            else:
                #print("MissCache",HSH)
                self.cur.execute('select NKey from {} where Nkey=\'{}\';'.format(self.TableName,HSH))

                Exist = len(self.cur.fetchall()) != 0

                #print("Exists? ",Exist)
                self.NameCache.put(HSH,Exist)
                

            #Act
            if Exist:
                Identity[HSH] = 1
            elif (not Exist) & AddNew:
                #print("Add",HSH)
                self.cur.execute('insert into {} (NKey,YWeight,NWeight) values (\'{}\',{},{});'.format(self.TableName,HSH,random.random(),random.random()))
                
                Identity[HSH] = 1
                self.NameCache.update(HSH,True)
                self.NameCache.toggleSync(HSH)
            else:
                pass
            
        self.db.commit()
        self.cur.execute('commit;')

        return Identity

    def syncer(self,Key,Mode):
        if Mode == "N":
            self.cur.execute('update {} set NWeight = {} where NKey like \'{}\';'.format(self.TableName,self.NWeightCache.fetch(Key),Key))
        else:
            self.cur.execute('update {} set YWeight = {} where NKey like \'{}\';'.format(self.TableName,self.YWeightCache.fetch(Key),Key))
        #print("UPDT")
        

    def train(self,Line,YRes,NRes,Splitter=splitter,sync=True):
        Identity = self._toIdent(Line,Splitter,True)
        self._train(Identity,YRes,NRes)

        if sync:
            self.NWeightCache.sync(self.syncer,"N")
            self.YWeightCache.sync(self.syncer,"Y")
            self.db.commit()

    def predict(self,Line,Splitter=splitter):
        Identity = self._toIdent(Line,Splitter)
        return self._predict(Identity)



        



    

if __name__ == '__main__':
    import getpass
    import gzip
    import sys
    import time

    CON = mc.connect(host = input("Host>"),
                user = input("User>"),
                passwd = getpass.getpass(),
                database = "LogProcDB2",
                port = int(input("Port>")))
    print("Connected")

    NL = NeuralLogger(CON,"FailClassify",0.001)

    load = 80000000
    f1 = gzip.open(sys.argv[1],"rb")
    f2 = gzip.open(sys.argv[2],"rb")

    st = time.time()
    cnt = 0
    for i in range(load):
        en = time.time()
        if en - st > 1:
            print(cnt/(en-st),"/s")
            cnt = 0
            st = en
            NL.NameCache.cleanCache()
            NL.NWeightCache.cleanCache()
            NL.YWeightCache.cleanCache()

            NL.NWeightCache.sync(NL.syncer,"N")
            NL.YWeightCache.sync(NL.syncer,"Y")
            NL.db.commit()

        cnt += 2

        f1.readlines(random.randint(1,30))
        f2.readlines(random.randint(1,30))

        L1 = f1.readline()
        if L1 == b'':
            f1.seek(0)
            L1 = f1.readline()
        L2 = f2.readline()
        if L2 == b'':
            f2.seek(0)
            L2 = f2.readline()
        
        NL.train(f1.readline(),1,0,sync=False)
        NL.train(f2.readline(),0,1,sync=False)
    
    print("Training Complete")

    f1.close()
    f2.close()
