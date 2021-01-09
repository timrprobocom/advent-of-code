import os
import re
import sys
from pprint import pprint

test = "1"
live = "1113222113"


DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = live

data = list(map(int,data))

def evolve(line):
    seq = []
    last = []
    for ch in line:
        if last and ch == last[0]:
            last.append(ch)
        else:
            if last:
                seq.extend([len(last),last[0]])
            last = [ch]
    seq.extend([len(last),last[0]])
    return seq

for i in range(40):
    data = evolve(data)
print( "Part 1:", len(data) )
for i in range(10):
    data = evolve(data)
print( "Part 2:", len(data) )
