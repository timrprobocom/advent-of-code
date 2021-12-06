import sys
from collections import Counter
from math import comb

test = [3,4,3,1,2]
live = [
1,4,1,1,1,1,5,1,1,5,1,4,2,5,1,2,3,1,1,1,1,5,4,2,1,1,3,1,1,1,1,1,1,1,2,1,1,1,1,1,5,1,1,1,1,1,1,1,1,1,4,1,1,1,1,5,1,4,1,1,4,1,1,1,1,4,1,1,5,5,1,1,1,4,1,1,1,1,1,3,2,1,1,1,1,1,2,3,1,1,2,1,1,1,3,1,1,1,2,1,2,1,1,2,1,1,3,1,1,1,3,3,5,1,4,1,1,5,1,1,4,1,5,3,3,5,1,1,1,4,1,1,1,1,1,1,5,5,1,1,4,1,2,1,1,1,1,2,2,2,1,1,2,2,4,1,1,1,1,3,1,2,3,4,1,1,1,4,4,1,1,1,1,1,1,1,4,2,5,2,1,1,4,1,1,5,1,1,5,1,5,5,1,3,5,1,1,5,1,1,2,2,1,1,1,1,1,1,1,4,3,1,1,4,1,4,1,1,1,1,4,1,4,4,4,3,1,1,3,2,1,1,1,1,1,1,1,4,1,3,1,1,1,1,1,1,1,5,2,4,2,1,4,4,1,5,1,1,3,1,3,1,1,1,1,1,4,2,3,2,1,1,2,1,5,2,1,1,4,1,4,1,1,1,4,4,1,1,1,1,1,1,4,1,1,1,2,1,1,2
]

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = live

def part1(n,data):
    data = data[:]
    for _ in range(n):
        for i in range(len(data)):
            if data[i] == 0:
                data[i] = 6
                data.append( 8 )
            else:
                data[i] -= 1
    return len(data)

# Combinations would not have occurred to me.
#
# 1 (the original)
#
# for i in 0 .. 1+t/7
#   for k in 0 .. 1+(t-7i)/9
#     So you count the combos if there's enough time?
#
# I don't understand this solution.

def descendants(t, v):
    return 1 + sum(comb(i + k, i) * ((v + i * 7 + k * 9) < t) for i in range(1 + t // 7) for k in range(1 + (t - i * 7) // 9))

def part2(n,data):
    return sum(descendants(n,d) for d in data)

def test2():
    for n in (80,256):
        for z in range(6):
            print(n, z, descendants(n,z) )

def oneday(lanternfisch):
    new_lanternfish = [0] * 9
    for index in range(len(lanternfisch)):
        if index == 0:
            new_lanternfish[6] += lanternfisch[0]
            new_lanternfish[8] += lanternfisch[0]
        else:
            new_lanternfish[index - 1] += lanternfisch[index]
    return new_lanternfish

def part2(n,data):
    counts = [0]*9
    for i in data:
        counts[i] += 1
    for i in range(n):
        counts = oneday(counts)
    return sum(counts)

print("Part 1:", part1(80,data))
print("Part 1:", part2(80,data))
print("Part 2:", part2(256,data))