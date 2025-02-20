import os
import sys
import math
import random
import collections

test = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

day = os.path.splitext(os.path.basename(__file__))[0]

if TEST:
    data = test.strip()
else:
    data = open('day25.txt').read().strip()

DEBUG = 'debug' in sys.argv

def shortestPath( graph, v1, v2 ):
    queue = [(v1,[v1])]
    seen = set()
    while queue:
        v,path = queue.pop(0)
        if v == v2:
            return path
        seen.add(v)
        for n in graph[v]:
            if n not in seen:
                queue.append( (n,path+[n]) )
    return None

def reachableNodes(graph, start):
    seen = set()
    queue = [start]
    seen.add( start )
    while queue:
        v = queue.pop(0)
        seen.add(v)
        for edge in graph[v]:
            if edge not in seen:
                queue.append(edge)
    return seen
            
def make_graph(data):
    graph = collections.defaultdict(list)
    for row in data.splitlines():
        parts = row.split()
        base = parts.pop(0).strip(':')
        for p in parts:
            graph[base].append( p )
            graph[p].append( base )
    return graph

# We repeatedly pick two random vertices and find the shortest path between them via BFS.
# Then pick the top k most travelled edges and remove these from the graph and
# check if we have succesfully made a k cut. If so return it, if not we continue
#
# noCrossings is how many crossings to collect statistics on per attempt
# k is stop when we find a k-cut

def minimumCut( graph, noCrossings, cut=3 ):
    canReach = set()
    keys = list(graph.keys())
    while 1:
        crossingCounts = collections.Counter()
        for i in range(noCrossings):
            v1 = random.choice(keys)
            v2 = v1
            while v1 == v2:
                v2 = random.choice(keys)

            print(v1,v2)
            path = shortestPath(graph,v1,v2)
            for p1,p2 in zip(path[1:],path[:-1]):
                crossingCounts[(p1,p2)] += 1

        # remove the 3 edges that we are guessing make the min cut
        g2 = {}
        topk = [k[0] for k in crossingCounts.most_common(cut)]
        for k,v in graph.items():
            g2[k] = v[:]
        for key in topk:
            if key[1] in g2[key[0]]:
                g2[key[0]].remove( key[1] )
            if key[0] in g2[key[1]]:
                g2[key[1]].remove( key[0] )

        canReach = reachableNodes(g2, keys[0])

        if len(canReach) < len(graph):
            break

    return canReach

def part1(data):
    graph = make_graph(data)
    one = minimumCut( graph, 20, 3 )
    one = len(one)
    two = len(graph) - one
    return one*two

print("Part 1:", part1(data))
