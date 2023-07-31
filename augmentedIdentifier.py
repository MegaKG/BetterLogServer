#!/usr/bin/env python3
import keywordIdentifier
import perceptronIdentifier


class identifier:
    def __init__(self,args,tablename):
        self.config = args
        self.tname = tablename

        self.kwIdent = keywordIdentifier.identifier(args,self.tname + '_KW')
        self.pcIdent = perceptronIdentifier.identifier(args,self.tname + '_PC')

        
    def assessLog(self,log,faculty):
        Result1 = self.kwIdent.assessLog(log,faculty)
        #print("Activated",Result1,log)
        if Result1:
            Result2 = self.pcIdent.assessLog(log,faculty)
            #print("RES2",Result2,log)
            return Result2
        return False
        
                
