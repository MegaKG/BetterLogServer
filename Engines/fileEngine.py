#!/usr/bin/env python3
import gzip
import os

class saver:
    def __init__(self, directory, filename = None):
        self.filename = filename
        self.directory = directory

    def saveLog(self,Log,MessageStamp,Faculty):
        if not os.path.exists(self.directory + '/' + str(MessageStamp.year)):
            os.mkdir(self.directory + '/' + str(MessageStamp.year))
        
        if not os.path.exists(self.directory + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month)):
            os.mkdir(self.directory + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month))

        if self.filename == None:
            f = gzip.open(self.directory + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month) + '/' + str(MessageStamp.day) + '.gz','ab')
            f.write(Log + b'\n')
            f.close()
        else:
            f = gzip.open(self.directory + '/' + str(MessageStamp.year) + '/' + str(MessageStamp.month) + '/' + self.filename + '.gz','ab')
            f.write(Log + b'\n')
            f.close()