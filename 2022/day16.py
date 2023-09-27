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

class Valve:
    def __init__(self, name, flow, tunnels):
        self.name = name
        self.flow = flow
        self.tunnels = tunnels
        self.open = False
    def __repr__(self):
        return f"<Valve {self.name} flow {self.flow} tunnels {self.tunnels}"

# Parse the input.

valveindex = {}

for line in data:
    groups = pat.match(line).groups()
    name = groups[0]
    valveindex[name] = Valve(name, int(groups[1]), groups[2].split(', '))

# Translate the tunnels to valve objects.

valves = list(valveindex.values())

for v in valves:
    v.tunnels = [valveindex[k] for k in v.tunnels]

def part1(t, pos, flow):
    global m
    
    if _seen.get((t, pos.name), -1) >= sum(flow):
        return max(m,sum(flow))
    _seen[t, pos.name] = sum(flow)
    
    # If we hit the end, return a value.

    if t == 30:
        m = max(m, sum(flow))
        if DEBUG:
            print(m)
        return m
    
    # Sum up the amount released by all the open valves.

    j = sum(v.flow for v in valves if v.open)

    # If there is an unopened useful valve here, open it.
    # See what the best options are with this valve being open.
                
    if not pos.open and pos.flow > 0:
        pos.open = True
        part1(
            t + 1,
            pos,
            flow + [ j+pos.flow ]
        )
        pos.open = False

    # For all possible moves from here, make the move and
    # see what happens.

    for v in pos.tunnels:
        part1(
            t + 1,
            v, 
            flow + [ j ]
        )

    return m

def part2(t, pos1, pos2, flow):
    global m

    if _seen.get((t, pos1.name, pos2.name), -1) >= sum(flow):
        return m
    _seen[t, pos1.name, pos2.name] = sum(flow)
    
    if t == 26:
        if sum(flow) > m:
            m = sum(flow)
            if DEBUG:
                print(m, flow)
        return m
    
    # If all openable valves are open, then do nothing.
    
    j = sum(v.flow for v in valves if v.open)

    if all( v.open or not v.flow for v in valves ):
        part2(t + 1, pos1, pos2, flow + [j])
        return m

    if not pos1.open and pos1.flow:
            
        pos1.open = True
        j += pos1.flow
        
        if not pos2.open and pos2.flow:
            pos2.open = True
            part2(
                t + 1,
                pos1,
                pos2,
                flow + [ j+pos2.flow ]
            )
            pos2.open = False
        for v2 in pos2.tunnels:
            part2(
                t + 1,
                pos1,
                v2,
                flow + [ j ]
            )

        pos1.open = False
    else:
        for v in pos1.tunnels:
            if not pos2.open and pos2.flow:
                pos2.open = True
                part2(
                    t + 1,
                    v,
                    pos2,
                    flow + [ j+pos2.flow ]
                )
                pos2.open = False
            for v2 in pos2.tunnels:
                part2(
                    t + 1,
                    v,
                    v2,
                    flow + [ j ]
                )
    return m

AA = valveindex['AA']

_seen = {}
m = 0
print("Part 1: ",part1(1, AA, [ 0 ]))
_seen = {}
m = 0
print("Part 2: ",part2(1, AA, AA, [ 0 ]))
