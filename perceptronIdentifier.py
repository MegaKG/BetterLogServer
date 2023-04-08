#!/usr/bin/env python3
import NeuralLoggerLib as NLL
import mysql.connector as mc

TrainingCollect = True

class identifier:
    def tableExists(self,Name):
        #Check if the Tables Exist
        self.cursor.execute("SHOW TABLES")
        TABLES = self.cursor.fetchall()

        Exists = False
        for i in TABLES:
            if i[0] == Name:
                Exists = True
        
        return Exists

    def __init__(self,args,tablename):
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

        #Create it if needed
        if not self.tableExists(self.tname):
            self.cursor.execute('CREATE TABLE {} (NKey char(64) NOT NULL,YWeight double DEFAULT NULL,NWeight double DEFAULT NULL,PRIMARY KEY (NKey));'.format(self.tname))

        #Check if the output table exists as well
        if not self.tableExists(self.tname + '_Output'):
            self.cursor.execute('CREATE TABLE {} (Message varchar(512) not null);'.format(self.tname + '_Output'))

        self.neuralLogger = NLL.NeuralLogger(self.db,self.tname,0.01)

    def assessLog(self,log,faculty):
        Result = self.neuralLogger.predict(log)
        Assessed = Result[0] > Result[1]

        #Keep a record of activated logs
        if TrainingCollect:
            self.cursor.execute("insert into {} values (%s)".format(self.tname + '_Output'), (log[:511],))

        return Assessed
        
                



            



