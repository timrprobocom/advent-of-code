import os
import sys


test = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".splitlines()

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
    preamble = 5
else:
    data = open('day09.txt').read().split('\n')[:-1]
    preamble = 25

data = [int(d) for d in data]

def part1(data):
    for i in range(preamble,len(data)):
        found = False
        for j in range(i-preamble,i):
            for k in range(j+1,i):
                if DEBUG:
                    print(i,j,k,data[i],data[j],data[i])
                if data[i] == data[j] + data[k]:
                    found = True
                    break
        if not found:
            return data[i]

    return None

def part2(data, key):
    # Start here.
    for i in range(len(data)):
        # End here.
        for j in range(i,len(data)):
            trial = sum(data[i:j])
            if trial == key:
                return min(data[i:j])+max(data[i:j])
            if trial > key:
                break


key = part1(data)
print( "Part 1:", key )
print( "Part 2:", part2(data,key) )
