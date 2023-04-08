#!/usr/bin/env python3

LaunchArgs = {
        'host':'0.0.0.0',
        'port':10514,
        'tcp':True,
        'udp':True,
        'maxlen':1024,

        'dbhost':'localhost',
        'dbuser':'loguser',
        'dbpass':'logpassword',
        'dbdata':'LogDB',
        'dbport':3306,
        'HourlyTable':'Hourly',


        'logOutDir':'./Logs',


        'Lookups':[
            {'type':'augmentedIdentifier', 'arguments':{'tablename':'AuthTable'}, 'engine':{'type':'fileEngine','arguments':{'filename':'AuthData'}}},
            {'type':'dummyIdentifier', 'arguments':{}, 'engine':{'type':'fileEngine','arguments':{}}}    
        ],


        'smtpserver':'',
        'email':'',
        'emailuser':'',
        'emailpass':'',
        'emailport':587,
        'emailtargets':[]
    }
