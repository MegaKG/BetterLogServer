#!/usr/bin/env python3
import NeuralLoggerLib as NLL
import mysql.connector as mc

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
            self.cursor.execute('CREATE TABLE {} (NKey char(64) NOT NULL,YWeight double DEFAULT NULL,NWeight double DEFAULT NULL,PRIMARY KEY (NKey));'.format(self.tname))


        self.neuralLogger = NLL.NeuralLogger(self.db,self.tname,0.01)

    def assessLog(self,log,faculty):
        Result = self.neuralLogger.predict(log)
        return Result[0] > Result[1]
        
                



            



