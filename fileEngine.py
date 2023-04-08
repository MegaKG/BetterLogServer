#!/usr/bin/env python3
import gzip
import os

class saver:
    def __init__(self,Config,filename = None):
        self.filename = filename
        self.Config = Config

    def saveLog(self,Log,MessageStamp):
        if not os.path.exists(self.Config['logOutDir'] + '/' + str(MessageStamp.year)):
            os.mkdir(self.Config['logOutDir'] + '/' + str(MessageStamp.year))
        
        if not os.path.exists(self.Config['logOutDir'] + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month)):
            os.mkdir(self.Config['logOutDir'] + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month))

        if self.filename == None:
            f = gzip.open(self.Config['logOutDir'] + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month) + '/' + str(MessageStamp.day) + '.gz','ab')
            f.write(Log + b'\n')
            f.close()
        else:
            f = gzip.open(self.Config['logOutDir'] + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month) + '/' + self.filename + '.gz','ab')
            f.write(Log + b'\n')
            f.close()