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
    def __init__(self,faculty):
        #In this case, the faculty is the faculty
        if faculty.lower() in FLOOKUP:
            self.myfaculty = FLOOKUP[faculty]
        else:
            self.myfaculty = int(faculty)


        
    def assessLog(self,log,priority):
        faculty = int(priority/8)
        severity = int(((priority/8) - faculty) * 8)
        if faculty == self.myfaculty:
            return True
        return False
        
                