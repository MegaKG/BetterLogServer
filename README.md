# BetterLogServer
A Python Logserver with configurable filters


Most of this is self explanatory.
The dictionary in Config.py is passed to most of the functions.

The files intended to be modified are logsaver.py, logvalidity.py and any of the optional Identifiers.

Logs follow this path:

Logserver.py -> Logvalidity.py -> Logserver.py -> Logsaver.py -> (Many Identifiers)

The engines at the moment are file: Save to file, or Email: save to file and Email.
