#!/usr/bin/env python3
import datetime

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

def parse(log):
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
            print("Parse Error",E,log)
        return False