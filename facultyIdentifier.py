#!/usr/bin/env python3
FLOOKUP = {
    'kernel':0,
    'user':1,
    'mail':2,
    'daemons':3,
    'security':4,
    'audit':13,
    'alert':14,
    'syslog':5
}

class identifier:
    def __init__(self,args,tablename):
        self.config = args
        

        #In this case, the tablename is the faculty
        if tablename.lower() in FLOOKUP:
            self.myfaculty = FLOOKUP[tablename]
        else:
            self.myfaculty = int(tablename)


        
    def assessLog(self,log,priority):
        faculty = int(priority/8)
        severity = int(((priority/8) - faculty) * 8)
        if faculty == self.myfaculty:
            return True
        return False
        
                