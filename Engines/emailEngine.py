#!/usr/bin/env python3
import Engines.EmailComposer as EmailComposer

class saver:
    def __init__(self,server,email,user,password,port,grouping=None):
        self.grouping = grouping

        if grouping == None:
            self.emailer = EmailComposer.emailer(server,email,user,password,port,"ALERT")
        else:
            self.emailer = EmailComposer.emailer(server,email,user,password,port,grouping)
        self.emailer.start()

    def saveLog(self,Log,MessageStamp,Faculty):
        self.emailer.appendUrgent(Log)