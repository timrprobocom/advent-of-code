import os
import sys
import functools
import operator

test = """\
16
10
15
5
1
11
7
19
6
12
4""".splitlines()

test2 = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".splitlines()

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = open('day10.txt').read().split('\n')[:-1]

data = [int(d) for d in data]
data.sort()
builtin = max(data) + 3
data = [0] + data + [builtin]

diffs = [data[i+1]-data[i] for i in range(len(data)-1)]

if DEBUG:
    print( diffs )

print( "Part 1:", diffs.count(1)*diffs.count(3))

# Two 1s can be 2 ways     1 1 or 2
# Three 1s can be 4 ways:  1 1 1 or 2 1 or 1 2 or 3
# Four 1s can be 7 ways:   1 1 1 1 or 1 1 2 or 1 2 1 or 2 1 1 or 1 3 or 3 1 or 2 2
# Five 1s can be 13 ways:  1 1 1 1 1 or 2 1 1 1 or 1 2 1 1 or 1 1 2 1 or 1 1 1 2 or 2 2 1 or 2 1 2 or 1 2 2 or
#                            3 1 1 or 1 3 1 or 1 1 3 or 3 2 or 2 3
# +1 +2 +3 +6 

mapping = { 2:2, 3:4, 4:7, 5:13 }

# Count sequences of 1s.

sequences = []
this = 0
for i in diffs:
    if i == 1:
        this += 1
    else:
        if this >= 2:
            sequences.append(this)
        this = 0

sets = [mapping[i] for i in sequences]

if DEBUG:
    print(sequences)
    print(sets)

print( "Part 2:", functools.reduce(operator.mul,sets))

# Why does this work?  
# It says the ways to get to N is the sum of the ways to get to the past 3.
# I suppose that's right.

stairs = [0] * (data[-1]+1)
stairs[0] = 1
for n in data[1:]:
    stairs[n] = stairs[n-3] + stairs[n-2] + stairs[n-1]
print( stairs )
