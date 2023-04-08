#!/usr/bin/env python3
import EmailComposer

class saver:
    def __init__(self,Config,grouping=None):
        self.grouping = grouping
        self.Config = Config

        if grouping == None:
            self.emailer = EmailComposer.emailer(self.Config,"ALERT")
        else:
            self.emailer = EmailComposer.emailer(self.Config,grouping)
        self.emailer.start()

    def saveLog(self,Log,MessageStamp):
        self.emailer.appendUrgent(Log)