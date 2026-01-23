import sys

DEBUG = 'debug' in sys.argv
TEST = 'test' in sys.argv

data = open('day3.txt').readlines()

def part1(data):
    counts = { True: 0, False: 0 }
    tries = []
    for ln in data:
        parts = list(int(k) for k in ln.strip().split())
        maxpart = max(parts)
        rest = sum(parts)-maxpart
        valid = rest > maxpart
        if DEBUG:
            print( valid, parts, maxpart, rest )
        counts[valid] += 1
    tries=[]
    return counts

def part2(data):
    counts = { True: 0, False: 0 }
    tries = []
    for ln in data:
        parts = list(int(k) for k in ln.strip().split())
        tries.extend( parts )
        if len(tries) == 9:
            for i in range(3):
                parts = [tries[i+0],tries[i+3],tries[i+6]]
                maxpart = max(parts)
                rest = sum(parts)-maxpart
                valid = rest > maxpart
                if DEBUG:
                    print( valid, parts, maxpart, rest )
                counts[valid] += 1
            tries=[]
    return counts

print( 'Part 1:', part1(data)[True] )
print( 'Part 2:', part2(data)[True] )

