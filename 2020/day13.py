import os
import sys
import functools
import operator
from tools import Point

test = """\
939
7,13,x,x,59,x,31,19"""

from pprint import pprint

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = open('day13.txt').read()

stamp,buses = data.split()
stamp = int(stamp)
buses = buses.split(',')

pairs = [(i,int(ln)) for i,ln in enumerate(buses) if ln != 'x']
posns = [i[0] for i in pairs]
buses = [i[1] for i in pairs]


# So how does this work?
# This computes x where x = ai mod ni for all i.

def chinese_remainder(n, a):
    sum = 0
    prod = functools.reduce(operator.mul, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
# This is the Extended Euclidean Algorithm for computing  multiplicative 
# inverse in a modulo field.  It is basically doing a GCD.

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 

print( buses )
print( posns )


def pass1():
    winline = 0
    wintime = 9999999999999
    for line in buses:
        poss = (stamp + line - 1) // line * line
        if poss < wintime:
            winline = line
            wintime = poss
    print( winline, wintime )
    return winline*(wintime-stamp)

print( "Part 1:", pass1() )
 
def pass2():
    rems = [ b-p for b,p in zip(buses,posns) ]
    return chinese_remainder(buses, rems)

print( "Part 2:", pass2() )

# So they are all equal again at 1,131,189,818,632,523.
#
# 0 1 3 5 6     1068781
#
# 7 and 13 are off by 6 then 5 then 4 then 3 then 2 then 1 then 0
# 7 and 59 are off by 4 then 1 then 5 then 2 then 6 then 3 then 0
# 7 and 31 are off by 4 then 1 then 5 then 2 then 6 then 3 then 0
# 7 and 19 are off by 2 then 4 then 6 then 1 then 3 then 5 then 0
#
# so 7 and 13 line up at 77 mod 91
# so 7 and 31 line up
# lcm?
#

