#!/usr/bin/env python3

LaunchArgs = {
        'host':'0.0.0.0',
        'port':10514,
        'tcp':True,
        'udp':True,
        'maxlen':1024,

        'dbhost':'localhost',
        'dbuser':'loguser',
        'dbpass':'password',
        'dbdata':'LogDB',
        'dbport':3306,
        'HourlyTable':'Hourly',


        'logOutDir':'/logserver/Logs',


        'Lookups':[
            {'type':'augmentedIdentifier', 'arguments':{'tablename':'AuthTable'}, 'engine':{'type':'fileEngine','arguments':{'filename':'AuthData'}}},
            {'type':'facultyIdentifier', 'arguments':{'tablename':'kernel'}, 'engine':{'type':'fileEngine','arguments':{'filename':'Kernel'}}},
            {'type':'facultyIdentifier', 'arguments':{'tablename':'security'}, 'engine':{'type':'fileEngine','arguments':{'filename':'Security'}}},
            {'type':'severityMinimumIdentifier', 'arguments':{'tablename':'critical'}, 'engine':{'type':'fileEngine','arguments':{'filename':'Important'}}},
            {'type':'dummyIdentifier', 'arguments':{}, 'engine':{'type':'fileEngine','arguments':{}}},
            {'type':'dummyIdentifier', 'arguments':{}, 'engine':{'type':'socketEngine','arguments':{}}}   
        ],


        'smtpserver':'',
        'email':'',
        'emailuser':'',
        'emailpass':'',
        'emailport':587,
        'emailtargets':[]
    }
