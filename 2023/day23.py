import os
import sys
import collections

test = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

data = data.splitlines()
HEIGHT = len(data)
WIDTH = len(data[0])
START = (1,0)
TARGET = (WIDTH-2,HEIGHT-1)

U,R,D,L = (0,-1),(1,0),(0,1),(-1,0)

DEBUG = 'debug' in sys.argv

valid1 = {}
valid2 = set()
for y,row in enumerate(data):
    for x,c in enumerate(row):
        if c != '#':
            valid2.add((x,y))
        if c == '.':
            valid1[(x,y)] = (U,R,D,L)
        elif c == '>':
            valid1[(x,y)] = [R]
        elif c == 'v':
            valid1[(x,y)] = [D]

def part1(data):
    queue = collections.deque([(START+(0,))])
    maxsize = 0
    seen = set()
    while queue:
        x,y,l = queue.pop()
        if l == -1:
            seen.remove((x,y))
        elif (x,y) == TARGET:
            maxsize = max(maxsize, l)
        elif (x,y) not in seen:
            seen.add((x,y))
            queue.append((x,y,-1))
            for dx,dy in valid1[(x,y)]:
                x1 = x+dx
                y1 = y+dy
                if (x1,y1) in valid1 and (x1,y1) not in seen and data[y1][x1] != '#':
                    queue.append( (x1,y1,l+1))
    return maxsize

# Make an adjacency graph.

def make_graph(data):
    graph = {}
    for y,row in enumerate(data):
        for x,c in enumerate(row):
            if c != '#':
                adj = {}
                for dx,dy in U,D,L,R:
                    x1 = x+dx
                    y1 = y+dy
                    if (x1,y1) in valid2:
                        adj[(x1,y1)] = 1
                graph[(x,y)] = adj
    return graph

# Optimize the graph by just connecting the hubs.

def optimize_graph(graph):
    hubs = {k for k,v in graph.items() if len(v) > 2}
    hubs.add(START)
    hubs.add(TARGET)

    # For each hub, find the next hubs in line.
    newgraph = {}
    for hx,hy in hubs:
        adj = []
        queue = [(hx,hy,1,set())]
        while queue:
            x,y,l,seen = queue.pop()
            if (x,y) in seen:
                continue
            seen = seen.union([(x,y)])
            for x1,y1 in graph[(x,y)].keys():
                if (x1,y1) not in seen:
                    if (x1,y1) in hubs:
                        adj.append( (x1,y1,l) )
                    else:
                        queue.append( (x1,y1,l+1,seen) )
        newgraph[(hx,hy)] = adj
    return newgraph

def part2(data):
    graph = make_graph(data)
    graph = optimize_graph(graph)

    queue = collections.deque([START+(0,)])
    maxsize = 0
    seen = set()
    while queue:
        x,y,l = queue.pop()
        if l < 0:
            seen.remove((x,y))
        elif (x,y) == TARGET:
            if l > maxsize:
                maxsize = l
                if DEBUG:
                    print(len(queue),maxsize)
        elif (x,y) not in seen:
            seen.add((x,y))
            queue.append( (x, y, -1) )
            for x1,y1,l1 in graph[(x,y)]:
                queue.append( (x1,y1,l+l1) )
    return maxsize
    
print("Part 1:", part1(data))
print("Part 2:", part2(data))