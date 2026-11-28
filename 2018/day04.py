import re
import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = [ln.strip() for ln in open('day04test.txt').readlines()]
live = [ln.strip() for ln in open('day04.txt').readlines()]


#[1518-02-03 23:50] Guard #661 begins shift
#[1518-02-04 00:01] falls asleep
#[1518-02-04 00:57] wakes up

data = test if TEST else live

# Parsing.

pat = r'['
guard = 0

def parse(ln):
    global guard
    parts = ln.split()
    hh,mm = list(int(k.strip(']')) for k in parts[1].split(':'))
    verb = parts[2]
    if verb == 'Guard':
        guard = int(parts[3][1:])
    return verb,guard,hh,mm

class track(object):
    def __init__(self, guard):
        self.guard = guard
        self.doze = 0
        self.when = [0]*60
    def __repr__(self):
        return '(track#%d, doze=%d, when=%s)' % (self.guard, self.doze,str(self.when))

sleeptime = {}

for ln in data:
    verb,guard,hh,mm = parse(ln)
    if verb == 'falls':
        sleep = mm
    elif verb == 'wakes':
        if guard not in sleeptime:
            sleeptime[guard] = track(guard)
        sleeptime[guard].doze += mm - sleep
        for minute in range(sleep,mm):
            sleeptime[guard].when[minute] += 1

if DEBUG:
    print(sleeptime)

# Find most asleep.

# Part 1

def part1(sleeptime):
    maxo = None
    for k,v in sleeptime.items():
        if not maxo or v.doze > maxo.doze:
            maxo = v

    maxn = -1
    maxp = 0
    for n,v in enumerate(maxo.when):
        if v > maxp:
            maxn = n
            maxp = v

    if DEBUG:
        print(maxo.guard)
        print(maxn)
        print('=', maxo.guard * maxn)
        print("----")
    return maxo.guard * maxn

# Find most commonly asleep minute.

# Part 2

def part2(sleeptime):
    maxn = [0] * 60
    maxz = [0] * 60
    for k,v in sleeptime.items():
        for mm,knt in enumerate(v.when):
            if knt > maxz[mm]:
                maxz[mm] = knt
                maxn[mm] = k

    maxval = max(maxz) 
    indval = maxz.index(maxval)
    if DEBUG:
        print( maxn[indval], indval, maxval, '=', maxn[indval] * indval)
    return maxn[indval] * indval

print( "Part 1:", part1(sleeptime))
print( "Part 2:", part2(sleeptime))
