#!/usr/bin/env python3
import UDPstreams3 as udp
import time

f = open('Logs.txt','rb')
CON = udp.clientCon('127.0.0.1',10514)
while True:
    L = f.read(512)
    print(L)
    if L == b'':
        break
    else:
        CON.senddat(L)
        time.sleep(0.1)
CON.close()
f.close()
