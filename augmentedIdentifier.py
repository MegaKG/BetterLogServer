#!/usr/bin/env python3
import keywordIdentifier
import perceptronIdentifier


class identifier:
    def __init__(self,tablename,args):
        self.config = args
        self.tname = tablename

        self.kwIdent = keywordIdentifier.identifier(self.tname + '_KW',args)
        self.pcIdent = perceptronIdentifier.identifier(self.tname + '_PC',args)

        
    def assessLog(self,log,faculty):
        Result1 = self.kwIdent.assessLog(log,faculty)
        if Result1:
            Result2 = self.pcIdent.assessLog(log,faculty)
            return Result2
        return False
        
                