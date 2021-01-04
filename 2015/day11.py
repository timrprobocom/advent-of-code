import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = "abcdefgh"
live = "vzbxkghb"

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = live

def encode(s):
    return [ord(i)-ord('a') for i in s]
def decode(s):
    return ''.join(chr(i+ord('a')) for i in s)

I = ord('i')-ord('a')
L = ord('l')-ord('a')
O = ord('o')-ord('a')

def isvalid(pw):
    return I not in pw and L not in pw and O not in pw and \
        any( a+2==b+1==c for a,b,c in zip(pw[:-2],pw[1:-1],pw[2:])) and \
        len( set( a for a,b in zip(pw[:-1],pw[1:]) if a==b )) >= 2

def cycle(pw):
    while 1:
        for i in range(len(pw)):
            if pw[-1-i] < 25:
                pw[-1-i] += 1
                break
            pw[-1-i] = 0
        if isvalid(pw):
            break
    return pw

if 'test' in sys.argv:
    print( isvalid(encode('hijklmn')), 0)
    print( isvalid(encode('abbceffg')), 0)
    print( isvalid(encode('abbcegjk')), 0)
    print( isvalid(encode("abcdffaa")), 1)
    print( isvalid(encode("ghjaabcc")), 1)
    print( decode(cycle(encode('abcdefgh'))), 'abcdffaa' )
    print( decode(cycle(encode('ghijklmn'))), 'ghjaabcc' )

pw = cycle(encode(data))
print( "Part 1", decode(pw) )
pw = cycle(pw)
print( "Part 2", decode(pw) )
