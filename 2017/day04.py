import sys
from collections import Counter

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = '''\
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa'''

live = open('day4.txt').read()

data = (test if TEST else live).splitlines()

def check(line):
    counts = Counter(line.split())
    return counts.most_common(1)[0][1] == 1

def check2(line):
    words = [''.join(sorted(w)) for w in line.split()]
    counts = Counter(words)
    return counts.most_common(1)[0][1] == 1

def part1(data):
    return sum(check(line) for line in data)

def part2(data):
    return sum(check2(line) for line in data)

print('Part 1:', part1(data))
print('Part 2:', part2(data))
