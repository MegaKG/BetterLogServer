#!/usr/bin/env python3
import time
import datetime
import mysql.connector as mc
import os
import gzip
import EmailComposer
import json


ReverseSeverity = {
    0:'Emergencies',
    1:'Criticals',
    2:'Alerts',
    3:'Errors',
    4:'Warnings',
    5:'Notices',
    6:'Information',
    7:'Debug'
}

MonthLookup = {
    b'Jan':1,
    b'Feb':2,
    b'Mar':3,
    b'Apr':4,
    b'May':5,
    b'Jun':6,
    b'Jul':7,
    b'Aug':8,
    b'Sep':9,
    b'Oct':10,
    b'Nov':11,
    b'Dec':12
}

class saver:
    def __init__(self, Config):
        self.config = Config
        self.Lookups = {}
        self.LookupEngines = {}

        self.Emailer = EmailComposer.emailer(Config)
        self.Emailer.start()

        self.config['LIBRARIES'] = {}
        for i in self.config['Lookups']:
            
            self.config['LIBRARIES'][i] = __import__(i)

            for a in self.config['Lookups'][i]:
                print("Enable Identifier",i,"for name",a['tablename'])
                self.Lookups[a['tablename']] = self.config['LIBRARIES'][i].identifier(a['tablename'],Config)
                self.LookupEngines[a['tablename']] = a['engine']

        self.MainCon = mc.connect(
                host = Config['dbhost'],
                user = Config['dbuser'],
                passwd = Config['dbpass'],
                database = Config['dbdata'],
                port = Config['dbport']
            )
        self.MainCursor = self.MainCon.cursor()

        self.HourlyStats = {
            'Machine Logs':{},
            'Total Logs':0,
            'Emergencies':0,
            'Alerts':0,
            'Criticals':0,
            'Errors':0,
            'Warnings':0,
            'Notices':0,
            'Information':0,
            'Debug':0,
            'Table Logs':{},
        }

        #Check if Hourly Table Exists
        self.MainCursor.execute("SHOW TABLES")
        TABLES = self.MainCursor.fetchall()

        Exists = False
        for i in TABLES:
            if i[0] == self.config['HourlyTable']:
                Exists = True
        #Create it if needed
        if not Exists:
            self.MainCursor.execute('CREATE TABLE {} (Timestamp INT(255) NOT NULL,Stats VARCHAR(1024) NOT NULL,PRIMARY KEY (Timestamp));'.format(self.config['HourlyTable']))


        self.LastUpd = time.time()

        

    def _parse(self,log):
        try:
            split = log.split(b'>')
            faculty = split[0]
            Log = b''
            for i in split[1:]:
                Log += i + b'>'
            Log = Log[:-1] 
            faculty = int(faculty.strip(b'<').decode())
            del split

            Date = Log[:16].replace(b'  ',b' ')
            log = Log[16:]
            del Log


            SP = Date.split(b' ')
            Month = MonthLookup[SP[0]]
            Day = int(SP[1].decode())

            Stamp = SP[2]
            SP = Stamp.split(b':')
            Hour = int(SP[0].decode())
            Minute = int(SP[1].decode())
            Second = int(SP[2].decode())

            #print(log)
            Machine = log.split(b' ')[0].decode().lower()


            return {'stamp':datetime.datetime(datetime.datetime.now().year,Month,Day,Hour,Minute,Second),'message':log,'priority':faculty,'machine':Machine}
        except Exception as E:
            print("Err",E,log)
        return False



    def log(self,data):
        try:
            #print(data)
            #print(self._parse(data))

            parsed = self._parse(data)

            #Save to main log now
            stamp = parsed['stamp']

            root = self.config['logOutDir']
            if str(stamp.year) not in os.listdir(root):
                os.mkdir(root + '/' + str(stamp.year))
            if str(stamp.month) not in os.listdir(root + '/' + str(stamp.year)):
                os.mkdir(root + '/' + str(stamp.year) + '/' + str(stamp.month))

            #Find Start of Data (Past Severity)
            count = 0
            for i in data:
                count += 1
                if i == ord('>'):
                    break

            file = gzip.open(root + '/' + str(stamp.year) + '/' + str(stamp.month) + '/' + str(stamp.day) + '.gz','ab')
            file.write(data[count:] + b'\n')
            file.close()

            #Check if we need to save it to other tables
            for i in self.Lookups:
                if self.Lookups[i].assessLog(parsed['message'],parsed['priority']):
                    #print("Lookup Match",i)

                    ENGINE = self.LookupEngines[i].lower()
                    if ENGINE == 'file':
                        file = gzip.open(root + '/' + str(stamp.year) + '/' + str(stamp.month) + '/' + i + '.gz','ab')
                        file.write(data[count:] + b'\n')
                        file.close()

                    elif ENGINE == 'email':
                        self.Emailer.appendUrgent(data[count:])

                    else:
                        print("Flag",data[count:])

                    if i not in self.HourlyStats['Table Logs']:
                        self.HourlyStats['Table Logs'][i] = 1
                    else:
                        self.HourlyStats['Table Logs'][i] += 1

            #Data Collection
            faculty = int(parsed['priority']/8)
            severity = int(((parsed['priority']/8) - faculty) * 8)
            
            self.HourlyStats['Total Logs'] += 1
            self.HourlyStats[ReverseSeverity[severity]] += 1

            if parsed['machine'] not in self.HourlyStats['Machine Logs']:
                self.HourlyStats['Machine Logs'][parsed['machine']] = 0
            
            self.HourlyStats['Machine Logs'][parsed['machine']] += 1

            #print(self.HourlyStats)

            if (time.time() - self.LastUpd) > (60*60):
                print("Submit Hourly")
                self.LastUpd = time.time()

                #print((int(self.LastUpd),json.dumps(self.HourlyStats)))
                self.MainCursor.execute('insert into {}(Timestamp,Stats) values (%s,%s);'.format(self.config['HourlyTable']),
                    (int(self.LastUpd),json.dumps(self.HourlyStats)))


                self.HourlyStats = {
                    'Machine Logs':{},
                    'Total Logs':0,
                    'Emergencies':0,
                    'Alerts':0,
                    'Criticals':0,
                    'Errors':0,
                    'Warnings':0,
                    'Notices':0,
                    'Information':0,
                    'Debug':0,
                    'Table Logs':{},
                }
        except Exception as E:
            print("Err2",E)


        

