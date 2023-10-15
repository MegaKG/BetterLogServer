#!/usr/bin/env python3
#This file contains an example config

#Import the saver Engines
import Engines.emailEngine
import Engines.fileEngine
import Engines.fileEngine
import Engines.socketEngine
import Engines.forwardEngine

#Import the Identifiers
import Identifiers.augmentedIdentifier
import Identifiers.dummyIdentifier
import Identifiers.facultyIdentifier
import Identifiers.keywordIdentifier
import Identifiers.perceptronIdentifier
import Identifiers.severityIdentifier
import Identifiers.severityMinimumIdentifier

MainFileSaver = Engines.fileEngine.saver("Logs")

LaunchArgs = {
    "servers":{
        "main":{
            'host':'0.0.0.0',
            'port':10514,
            'tcp':True,
            'udp':True,
            'maxLen':1024,
            'maxThreads':128,
            'deduplicateQueue':1000,

            'Handlers':{
                'Forwarder':{
                    "Identifier":Identifiers.dummyIdentifier.identifier(), 
                    "Engine":Engines.forwardEngine.saver('192.168.0.1')
                },
                'Kernel Events':{
                    "Identifier":Identifiers.facultyIdentifier.identifier("kernel"), 
                    "Engine":Engines.fileEngine.saver("Logs","Kernel")
                },
                'Local Socket':{
                    "Identifier":Identifiers.dummyIdentifier.identifier(),
                    "Engine":Engines.socketEngine.saver("/var/run/logserver")
                },
                'Security Events':{
                    "Identifier":Identifiers.facultyIdentifier.identifier("security"), 
                    "Engine":Engines.fileEngine.saver("Logs","Security")
                },
                'All Logs':{
                    "Identifier":Identifiers.dummyIdentifier.identifier(), 
                    "Engine":Engines.fileEngine.saver("Logs")
                }
            },

            'Statistics':[
                
            ]

        }
    }
}
