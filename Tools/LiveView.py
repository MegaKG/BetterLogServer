#!/usr/bin/env python3
import sys
import UNIXstreams4
sock = '/run/logserver'


if len(sys.argv) > 1:
    sock = sys.argv[1]

CON = UNIXstreams4.clientCon(sock)

while True:
    D = CON.getdat()
    if D == b'':
        break
    else:
        try:
            print(D.decode('utf-8').replace('\n','').replace('\r',''))
        except Exception as E:
            pass

CON.close()
