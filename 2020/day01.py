#! /usr/bin/env python3

import sys

test = [
1721,
979,
366,
299,
675,
1456
]

DEBUG = 'debug' in sys.argv
TEST = 'test' in sys.argv

live = [int(i) for i in open('day01.txt').readlines()]
if TEST:
    data = test
else:
    data = live

def pass1(data):
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            if data[i]+data[j] == 2020:
                return data[i]*data[j]

def pass2(data):
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            for k in range(j+1,len(data)):
                if data[i]+data[j]+data[k] == 2020:
                    return data[i]*data[j]*data[k]

print( "Pass 1:", pass1(data) )
print( "Pass 2:", pass2(data) )
