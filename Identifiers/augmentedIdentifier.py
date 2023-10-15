#!/usr/bin/env python3
import Identifiers.keywordIdentifier as kId
import Identifiers.perceptronIdentifier as pId


class identifier:
    def __init__(self,dbhost,dbuser,dbpass,dbdatabase,dbport,tablename):
        self.tname = tablename

        self.kwIdent = kId.keywordIdentifier.identifier(dbhost,dbuser,dbpass,dbdatabase,dbport,self.tname + '_KW')
        self.pcIdent = pId.perceptronIdentifier.identifier(dbhost,dbuser,dbpass,dbdatabase,dbport,self.tname + '_PC')

        
    def assessLog(self,log,faculty):
        Result1 = self.kwIdent.assessLog(log,faculty)
        #print("Activated",Result1,log)
        if Result1:
            Result2 = self.pcIdent.assessLog(log,faculty)
            #print("RES2",Result2,log)
            return Result2
        return False
        
                
