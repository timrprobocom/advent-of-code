import os
import sys
from pprint import pprint

live = [0,20,7,16,1,18,15]

DEBUG = 'debug' in sys.argv

#Given the starting numbers 0,3,6, the 2020th number spoken is 465.
#Given the starting numbers 1,3,2, the 2020th number spoken is 1.
#Given the starting numbers 2,1,3, the 2020th number spoken is 10.
#Given the starting numbers 1,2,3, the 2020th number spoken is 27.
#Given the starting numbers 2,3,1, the 2020th number spoken is 78.
#Given the starting numbers 3,2,1, the 2020th number spoken is 438.
#Given the starting numbers 3,1,2, the 2020th number spoken is 1836.

#Given 0,3,6, the 30000000th number spoken is 175594.
#Given 1,3,2, the 30000000th number spoken is 2578.
#Given 2,1,3, the 30000000th number spoken is 3544142.
#Given 1,2,3, the 30000000th number spoken is 261214.
#Given 2,3,1, the 30000000th number spoken is 6895259.
#Given 3,2,1, the 30000000th number spoken is 18.
#Given 3,1,2, the 30000000th number spoken is 362.

if len(sys.argv) > 1:
    data = [int(k) for k in sys.argv[1:]]
else:
    data = live

def run(data, count):
    tape = len(data) - 1
    found = dict( (t,i+1)  for i,t in enumerate(data[:-1]))
    nextx = data[-1]
    while tape < count - 1:
        if tape % 500000 == 0:
            print( '  %d%%' % (tape * 100 / count), end='\r' )
        tape += 1
        lastx = found[nextx] if nextx in found else tape
        found[nextx] = tape
        nextx = tape - lastx

    return nextx

print( "Pass 1:", run(data,2020), '    ' )
print( "Pass 2:", run(data,30000000), '    ' )
