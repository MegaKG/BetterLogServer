#!/usr/bin/env python3
FLOOKUP = {
    'emergency':0,
    'alert':1,
    'critical':2,
    'error':3,
    'warning':4,
    'notice':5,
    'info':6,
    'debug':7
}

class identifier:
    def __init__(self,severity):

        #In this case, the severity is the faculty
        if severity.lower() in FLOOKUP:
            self.severity = FLOOKUP[severity]
        else:
            self.severity = int(severity)


        
    def assessLog(self,log,priority):
        faculty = int(priority/8)
        severity = int(((priority/8) - faculty) * 8)
        if severity <= self.severity:
            return True
        return False
        
                
