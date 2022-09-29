#!/usr/bin/env python3

LaunchArgs = {
        'host':'0.0.0.0',
        'port':1514,
        'tcp':True,
        'udp':True,
        'maxlen':1024,

        'dbhost':'127.0.0.1',
        'dbuser':'python',
        'dbpass':'python',
        'dbdata':'LogDB',
        'dbport':3306,
        'HourlyTable':'Hourly',

        'logOutDir':'.',

        #Engines are 'file' or 'email'
        #Table names must be unique
        'Lookups':{
            'augmentedIdentifier'   :[{'tablename':'ErrorTable','engine':'file'}],
            'keywordIdentifier'     :[{'tablename':'Test','engine':'file'}],
            'facultyIdentifier'     :[{'tablename':'kernel','engine':'email'}],
            'perceptronIdentifier'  :[{'tablename':'Test2','engine':'file'}],
            'severityIdentifier'    :[{'tablename':'emergency','engine':'file'}]
        },

        'smtpserver':'example.com',
        'email':'logserver@example.com',
        'emailuser':'logserver',
        'emailpass':'logpassword',
        'emailport':587,
        'emailtargets':['admin@example.com']
    }
