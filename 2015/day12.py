import os
import re
import sys
import json
import functools
import itertools
import operator
from pprint import pprint

test = (
"[1,2,3]",
'{"a":2,"b":4}',
'[[[3]]]',
'{"a":{"b":4},"c":-1}',
'{"a":[-1,1]}',
'[-1,{"a":1}]',
'[]',
'{}',
)


DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = [open('day12.txt').read()]

def count(ln):
    nums = re.findall(r'-*\d\d*', ln )
    return sum(map(int,nums))

def pass1(data):
    return sum( count(ln) for ln in data)

def check(obj):
    if type(obj) == int:
        return obj
    elif type(obj) == list:
        return sum(map(check,obj))
    elif type(obj) == dict and 'red' not in obj.values():
        return sum(map(check,obj.values()))
    return 0

def pass2(data):
    return sum( check( json.loads(ln) ) for ln in data )

print( "Part 1:", pass1(data) )
print( "Part 2:", pass2(data) )
