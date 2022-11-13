#!/usr/bin/env python3
import NeuralLoggerLib as NLL
import mysql.connector as mc
import sys
import Config
import time
import gzip

def similarityScore(A,B):
    Len = max([len(A),len(B)])
    Min = min([len(A),len(B)])
    Match = 0
    for i in range(Min):
        if A[i] == B[i]:
            Match += 1
    
    return Match/Len


def main():
    Results = {}
    args = Config.LaunchArgs

    if len(sys.argv) < 3:
        print("Usage: {} SourceFile.txt TableName")
        return
    
    DBConnection = mc.connect(
                host = args['dbhost'],
                user = args['dbuser'],
                passwd = args['dbpass'],
                database = args['dbdata'],
                port = args['dbport']
            )
    print("Connected To Database!")

    #Initialise the Neural Network
    NL = NLL.NeuralLogger(DBConnection,sys.argv[2])
    print("Initialised Neural Link")

    #Open the File
    f = gzip.open(sys.argv[1],'r')
    print("Found File")

    #Count all Lines
    LineCount = 0
    while True:
        L = f.readline()
        if L == b'':
            break
        else:
            LineCount += 1
    
    f.seek(0)
    print("Got Line Count",LineCount)

    #Now work through the file


    for i in range(LineCount):
        L = f.readline()
        print((i/LineCount)*100,"% Complete")
        print(L)

        Flag = False
        for a in Results:
            #print("Search",a,similarityScore(L,a))
            if similarityScore(L,a) > 0.75:
                YResult = Results[a][0]
                NResult = Results[a][1]
                Flag = True
                break


        if Flag:
            pass
        else:
            Res = ''
            while True:
                Res = input("\t(B)ad / (G)ood? ").lower()
                if Res in ['g','b']:
                    break

            YResult = int(Res == 'g')
            NResult = int(Res == 'b')

            Results[L] = [YResult,NResult]


        NL.train(L,YResult,NResult)
        print("Next")


    f.close()
    print("Closed Up")


if __name__ == '__main__':
    main()
