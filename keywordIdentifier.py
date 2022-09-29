#!/usr/bin/env python3
import mysql.connector as mc
import hashlib
import time

class record:
    def __init__(self,value):
        self.lastTime = time.time()
        self.value = value
        self.needSync = False

    def get(self):
        self.lastTime = time.time()
        return self.value

    def isDead(self):
        if not self.needSync:
            if (time.time() - self.lastTime) > 600:
                return True
            return False

        return False

    def getSyncStatus(self):
        return self.needSync

    def set(self,value):
        self.value = value
        self.needSync = True

    def unflag(self):
        self.needSync = False

    def flag(self):
        self.needSync = True

class cache:
    def __init__(self,dbcursor,tablename):
        self.cache = {}
        self.dbcursor = dbcursor
        self.tablename = tablename
        self.hits = 0
        self.misses = 0
        self.lastSync = time.time()


    def getWord(self,key):
        #Automated Sync first
        if (time.time() - self.lastSync) > 60:
            self.sync()


        if key in self.cache:
            if not self.cache[key].isDead():
                self.hits += 1
                #print("HIT")
                return self.cache[key].get()
        self.dbcursor.execute('select WTYPE from {} where WHASH=%s;'.format(self.tablename),(key,))
        result = self.dbcursor.fetchall()

        #Check if it is present
        self.misses += 1
        #print("MISS")
        if len(result) == 0:
            self.cache[key] = record(-1)
            self.cache[key].unflag() #Ensure that it isn't synced
            return -1

        else:
            value = int(result[0][0])
            self.cache[key] = record(value)
            return value

    def setWord(self,key,value):
        if key in self.cache:
            self.cache[key].set(value)
        else:
            self.cache[key] = record(value)
            self.cache[key].flag()

    def sync(self):
        print("Hits",self.hits,"Misses",self.misses)
        #Sync
        for i in self.cache:
            if self.cache[i].getSyncStatus():
                self.dbcursor.execute('INSERT INTO {} (WHASH, WTYPE) VALUES(%s, %i) ON DUPLICATE KEY UPDATE WTYPE=%i;'.format(self.tablename),(i,self.cache[i].get()))
                self.cache[i].unflag()


        #Remove Old Records
        KillList = []
        for i in self.cache:
            if self.cache[i].isDead():
                KillList.append(i)

        for i in KillList:
            del self.cache[i]

        self.lastSync = time.time()

        





class identifier:
    def __init__(self,tablename,args):
        self.config = args
        self.tname = tablename

        self.db = mc.connect(
                host = args['dbhost'],
                user = args['dbuser'],
                passwd = args['dbpass'],
                database = args['dbdata'],
                port = args['dbport']
            )

        self.cursor = self.db.cursor()

        #Check if the Tables Exist
        self.cursor.execute("SHOW TABLES")
        TABLES = self.cursor.fetchall()

        Exists = False
        for i in TABLES:
            if i[0] == self.tname:
                Exists = True
        #Create it if needed
        if not Exists:
            self.cursor.execute('create table {} ( WHASH CHAR(64) NOT NULL, WTYPE INT NOT NULL, PRIMARY KEY (WHASH) );'.format(self.tname))

        self.cache = cache(self.cursor,self.tname)

    def assessLog(self,log,faculty):
        Trigger = False
        for word in log.split(b' '):
            hash = hashlib.sha256(word).hexdigest()
            result = self.cache.getWord(hash)

            #Ignore Missing lookups
            if result >= 0:
                if result == 1:
                    #Set the Trigger
                    Trigger = True
                else:
                    #Ignore always
                    Trigger = False
                    break
        return Trigger
                



            



