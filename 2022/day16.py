import re
import sys

test = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day16.txt').readlines()]

DEBUG = 'debug' in sys.argv

pat = re.compile('Valve ([A-Z][A-Z]) has flow rate=(\d*); tunnels? leads? to valves? ([A-Z, ]*)$')

# This is not my code.  I need to figure out how it works.

# These should be a structure.  Simplifies some of the code, I think.
# Make the tunnels be actual links.

Fs = {}
Vs = {}
Os = {}

for line in data:
    groups = pat.match(line).groups()
    name = groups[0]
    Fs[name] = int(groups[1])
    Vs[name] = groups[2].split(', ')
    Os[name] = False

def part1(t, pos, flow):
    global m
    
    if _seen.get((t, pos), -1) >= sum(flow):
        return max(m,sum(flow))
    _seen[t, pos] = sum(flow)
    
    # If we hit the end, return a value.

    if t == 30:
        m = max(m, sum(flow))
        if DEBUG:
            print(m)
        return m
    
    # Open valve here?

# Sum up the amount released by all the open valves.

    j = sum(Fs[k] for k, v in Os.items() if v)

# If there is an unopened useful valve here, open it.
# See what the best options are with this valve being 
# open.  (Why would you ever NOT open a valve?)
                
    if not Os[pos] and Fs[pos] > 0:
        Os[pos] = True
        part1(
            t + 1,
            pos,
            flow + [ j+Fs[pos] ]
        )
        Os[pos] = False

# For all possible moves from here, make the move and
# see what happens.

    for v in Vs[pos]:
        part1(
            t + 1,
            v, 
            flow + [ j ]
        )

    return m

def part2(t, pos1, pos2, flow):
    global m
    
    if _seen.get((t, pos1, pos2), -1) >= sum(flow):
        return m
    _seen[t, pos1, pos2] = sum(flow)
    
    if t == 26:
        if sum(flow) > m:
            m = sum(flow)
            if DEBUG:
                print(m, flow)
        return m
    
    # all open? just stay put...
    if all(v for k, v in Os.items() if Fs[k] > 0):
        tf = sum(Fs[k] for k, v in Os.items() if v)
        part2(t + 1, pos1, pos2, flow + [tf])
        return m
    
    j = sum(Fs[k] for k, v in Os.items() if v)

    if not Os[pos1] and Fs[pos1] > 0:
            
        Os[pos1] = True
        j += Fs[pos1]
        
        if not Os[pos2] and Fs[pos2] > 0:
            Os[pos2] = True
            part2(
                t + 1,
                pos1,
                pos2,
                flow + [ j+Fs[pos2] ]
            )
            Os[pos2] = False
        for v2 in Vs[pos2]:
            part2(
                t + 1,
                pos1,
                v2,
                flow + [ j ]
            )

        Os[pos1] = False
    else:
        for v in Vs[pos1]:
            if not Os[pos2] and Fs[pos2] > 0:
                Os[pos2] = True
                part2(
                    t + 1,
                    v,
                    pos2,
                    flow + [ j+Fs[pos2] ]
                )
                Os[pos2] = False
            for v2 in Vs[pos2]:
                part2(
                    t + 1,
                    v,
                    v2,
                    flow + [ j ]
                )
    return m

_seen = {}
m = 0
print("Part 1: ",part1(1, "AA", [ 0 ]))
_seen = {}
m = 0
print("Part 2: ",part2(1, "AA", "AA", [ 0 ]))
