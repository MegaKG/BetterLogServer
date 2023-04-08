#!/usr/bin/env python3
import time
import mysql.connector as mc
import EmailComposer
import hashlib
import LogParser


class identifierSaverPair:
    def __init__(self,Identifier,Saver):
        self.Identifier = Identifier
        self.Saver = Saver

    def process(self,Log):
        Parsed = LogParser.parse(Log)
        Stamp = Parsed['stamp']

        #Find the Start of the Message
        counter = 0
        for ch in Log:
            counter += 1
            if ch == ord('>'):
                break
            
        if self.Identifier.assessLog(Parsed['message'],Parsed['priority']):
            self.Saver.saveLog(Log[counter:],Stamp)


def sha256(IN):
 return hashlib.sha256(IN).hexdigest()


class saver:
    def __init__(self, Config):
        self.config = Config
        self.lastHash = ''


        #Load all the libraries
        self.Libraries = {}
        for rule in self.config['Lookups']:
            if rule['type'] not in self.Libraries:
                print("Enable Identifier",rule['type'])
                self.Libraries[rule['type']] = __import__(rule['type'])
            
            if rule['engine']['type']:
                if rule['engine']['type'] not in self.Libraries:
                    print("Enable Saver",rule['engine']['type'])
                    self.Libraries[rule['engine']['type']] = __import__(rule['engine']['type'])


        #Load all the Savers
        self.Savers = []
        for rule in self.config['Lookups']:
            Pair = identifierSaverPair(
                self.Libraries[rule['type']].identifier(self.config,**rule['arguments']),
                self.Libraries[rule['engine']['type']].saver(self.config,**rule['engine']['arguments'])
            )
            self.Savers.append(Pair)

        self.LastUpd = time.time()



    def log(self,data):
        try:
            #print(data)
            #print(self._parse(data))

            parsed = LogParser.parse(data)

            hsh = sha256(parsed['message'])
            if hsh == self.lastHash:
             #print("Block",parsed['message'])
             return
            self.lastHash = hsh

            #Save to main log now
            stamp = parsed['stamp']

            root = self.config['logOutDir']


            #Check if we need to save it to other tables
            for mySaver in self.Savers:
                mySaver.process(data)
            

        except Exception as E:
            print("Saver Error",E)
            #raise

        

