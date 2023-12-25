import os
import sys
import math
import networkx as nx

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
    data = open(day+'.txt').read().strip()

DEBUG = 'debug' in sys.argv

# I should learn more about networkx.

def part1(data):
    graph = nx.Graph()
    for row in data.splitlines():
        parts = row.split()
        base = parts.pop(0).strip(':')
        for p in parts:
            graph.add_edge( base, p )
    if DEBUG:
        print(graph)
    cuts = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(cuts)
    return math.prod(len(x) for x in nx.connected_components(graph))

print("Part 1:", part1(data))
