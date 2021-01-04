import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds. """.splitlines()


DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
    limit = 1000
else:
    data = open('day14.txt').read().split('\n')[:-1]
    limit = 2503

m = re.compile(r'(\S*)\D*(\d*)\D*(\d*)\D*(\d*)\D*')

class Reindeer(object):
    def __init__(self, name, rate, tfly, trest ):
        self.name = name
        self.rate = rate
        self.tfly = tfly
        self.trest = trest
        self.position = 0
        self.points = 0

    def __repr__(self):
        return f"({self.name} at {self.position}, {self.tfly}/{self.trest})"

    def advance(self,t0,t1):
        dt = t0 % (self.tfly + self.trest)
        if dt < self.tfly:
            dprint("%s moves by %d" % (self.name, (t1-t0) * self.rate ) )
            self.position += (t1-t0) * self.rate

def parse(data):
    team = []
    for ln in data:
        parts = m.match(ln)
        dprint( parts.groups() )
        team.append( Reindeer( parts[1], int(parts[2]), int(parts[3]), int(parts[4]) ))
    return team

team = parse(data)
for timex in range(limit):
    for r in team:
        r.advance(timex,timex+1)
    ahead = max( r.position for r in team )
    for r in team:
        if r.position == ahead:
            r.points += 1

print( "Part 1:", max(r.position for r in team) )
print( "Part 2:", max(r.points for r in team) )
