#!/usr/bin/env python3
import gzip
import multiprocessing
import os
import sys

def numericScore(Line):
    MonthLookup = {
        'Jan':1,
        'Feb':2,
        'Mar':3,
        'Apr':4,
        'May':5,
        'Jun':6,
        'Jul':7,
        'Aug':8,
        'Sep':9,
        'Oct':10,
        'Nov':11,
        'Dec':12
        }
    while b'  ' in Line:
        Line = Line.replace(b'  ',b' ')
        
    SP = Line.split(b' ')

    Month = MonthLookup[SP[0].decode('utf-8')]
    Day = int(SP[1].decode('utf-8'))
    
    Time = SP[2].decode('utf-8')
    TSP = Time.split(':')
    
    Hour = int(TSP[0])
    Minute = int(TSP[1])
    Second = int(TSP[2])

    Stamp = (
        1e0 * Second + 
        1e2 * Minute + 
        1e4 * Hour + 
        1e6 * Day +
        1e8 * Month
        )
    return Stamp


def processFile(FileName):
    f = gzip.open(FileName,'rb')

    LineArray = []

    #Read the positions of the start of every line
    while True:
        LineArray.append(f.tell())
        if f.readline() == b'':
            break

    f.seek(0)

    def readIndex(Index):
        try:
            f.seek(Index)
            line = f.readline()
            return numericScore(line)
        except Exception as E:
            return -1

    print("Read File Positions",FileName)

    #Here we do a quicksort
    g = gzip.open(FileName + '.tmp','wb')

    def quickSort(Array):
        #print("Array",len(Array))
        if len(Array) <= 1:
            return Array
        
        Pivot = readIndex(Array[int(len(Array)/2)])
        if Pivot > 0:
        
            LowBucket = []
            HighBucket = []
            SameBucket = []

            for element in Array:
                value = readIndex(element)
                if value < Pivot:
                    LowBucket.append(element)
                elif value > Pivot:
                    HighBucket.append(element)
                elif value == Pivot:
                    SameBucket.append(element)

            return quickSort(LowBucket) + SameBucket + quickSort(HighBucket)
        return []

    
    SortedIndexes = quickSort(LineArray)
    print("Sorted The Indexes",FileName)

    for key in SortedIndexes:
        f.seek(key)
        Line = f.readline()
        g.write(Line)

    print("Done",FileName)

    f.close()
    g.close()

    #Copy the File
    os.remove(FileName)
    os.rename(FileName + '.tmp', FileName)
    print("Renamed",FileName)

if __name__ == '__main__':
    cpu_count = multiprocessing.cpu_count()
    print("System has",cpu_count,"CPUs")

    def recurse(IN):
        files = os.listdir(IN)
        Out = []
        for i in files:
            v = IN + '/' + i
            if os.path.isdir(v):
                Out += recurse(v)
            else:
                if '.gz' in i:
                    print("Find",v)
                    Out.append(v)
        return Out

    Files = recurse(sys.argv[1])

    pool = multiprocessing.Pool(cpu_count)
    pool.map(processFile,Files)

