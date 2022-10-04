#!/usr/bin/env python3

LaunchArgs = {
        'host':'0.0.0.0',
        'port':514,
        'tcp':True,
        'udp':True,
        'maxlen':1024,

        'dbhost':'localhost',
        'dbuser':'loguser',
        'dbpass':'logpasswd',
        'dbdata':'LogDB',
        'dbport':3306,
        'HourlyTable':'Hourly',


        'logOutDir':'Logs',

        #Engines are 'file' or 'email'
        #Table names must be unique
        'Lookups':{
            'augmentedIdentifier'   :[{'tablename':'ErrorTable','engine':'file'}],
            #'keywordIdentifier'     :[{'tablename':'Test','engine':'file'}],
            'facultyIdentifier'     :[{'tablename':'kernel','engine':'file'},{'tablename':'security','engine':'email'}],
            #'perceptronIdentifier'  :[{'tablename':'Test2','engine':'file'}],
            'severityMinimumIdentifier'    :[{'tablename':'critical','engine':'email'}]
        },

        'smtpserver':'example.com',
        'email':'logserver@example.com',
        'emailuser':'logserver',
        'emailpass':'logpasswd',
        'emailport':587,
        'emailtargets':['admin@example.com']
    }
