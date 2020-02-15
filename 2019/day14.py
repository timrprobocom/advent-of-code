import os
import sys
from collections import defaultdict
from pprint import pprint

#13312 ORE for 1 FUEL:

test1="""\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

#180697 ORE for 1 FUEL:

test2="""\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

#2210736 ORE for 1 FUEL:

test3="""\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""


# Topological sort.

class Graph(object):
    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = set()

    def addEdge( self, u, v ):
        self.nodes.add( u )
        self.nodes.add( v )
        self.graph[u].append(v)

    def topoSortUtil(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self.topoSortUtil(i, visited, stack)
        stack.insert( 0, v )

    def topoSort( self ):
        # Mark all vertices not visited.
        visited = dict(zip( self.nodes, (False for i in self.nodes )))
        stack = []

        for i in self.nodes:
            if not visited[i]:
                self.topoSortUtil( i, visited, stack )

        return stack



TRACE = 'trace' in sys.argv[1:]
TEST = 'test' in sys.argv[1:]

class Mix(object):
    def __init__(self, sym, qty ):
        self.sym = sym
        self.qty = qty
        self.needs = {}
    def __repr__(self):
        s ="<Mix %s x %d from " % (self.sym,self.qty)
        s += (' + '.join('%s %d' % (a,b) for a,b in self.needs.items() ) )
        s += ">"
        return s

def parse(s):
    tree = {}
    graph = Graph()
    for ln in s.splitlines():
        lll,rrr = ln.split(' => ')
        q,sym = rrr.split(' ')
        chem = Mix(sym,int(q))
        tree[sym] = chem

        for part in lll.split(', '):
            q,sym = part.split(' ')
            graph.addEdge( chem.sym, sym )
            chem.needs[sym] = int(q)
    return tree, graph.topoSort()

# OK.  

def processloop(tree, amts, chem ):
    qty = amts[chem]
    amts[chem] = 0
    if TRACE:
        print( f"{qty} of {chem} needs:" )
    mix = tree[chem]
    qty = (qty+mix.qty-1) // mix.qty
    if TRACE:
        print( f"   {qty} units" )
    for a,b in mix.needs.items():
        if TRACE:
            print( f"   {b*qty} of {a}" )
        amts[a] += b*qty

def process( s, target ):
    tree, order = parse(s)
    if TRACE:
        print( order )
    amts = defaultdict(int)
    amts["FUEL"] = target
    amts["ORE"] = 0

    for i in order:
        if i == 'ORE':
            break
        processloop(tree, amts, i )
        if TRACE:
            print( "Stores: ", end='' )
            for k in order:
                print( f"'{k}': {amts[k]}, ", end='' )
            print()
#            print( amts["ORE"] )
    return amts["ORE"]
real = open('day14.txt').read()

if TEST:
    print( "Test 1: ", process(test1, 1) )
    print( "Test 2: ", process(test2, 1) )
    print( "Test 3: ", process(test3, 1) )
print( "*** Part 1: ", process(real,1) )


def part2( setup ):
    ore = 1000000000000
    guess = 1
    # Times 10 until we go over.

    while 1:
        got = process( setup, guess )
        if TRACE:
            print( f"{guess} got {got}" )
        if got > ore:
            break
        guess *= 10

    # Back down and do one digit at a time.

    guess //= 10
    incr = guess

    while incr:
        guess += incr
        got = process( setup, guess )
        if TRACE:
            print( f"{guess} got {got}" )
        if got > ore:
            guess -= incr
            incr //= 10
    return guess



if TEST:
    print( "Test 1: ", part2( test1 ) )
    print( "Test 2: ", part2( test2 ) )
    print( "Test 3: ", part2( test3 ) )
print( "*** Part 2: ", part2( real ) )
