
#
# Topological sort.
#

import itertools

test = (
'Step C must be finished before step A can begin.',
'Step C must be finished before step F can begin.',
'Step A must be finished before step B can begin.',
'Step A must be finished before step D can begin.',
'Step B must be finished before step E can begin.',
'Step D must be finished before step E can begin.',
'Step F must be finished before step E can begin.'
)

live = open('day07.txt').readlines()

def pull(ln):
    parts = ln.split()
    return parts[1],parts[7]

class Node(object):
    def __init__(self, c):
        self.next = []
        self.prev = []
    def __repr__(self):
        return  "(next=" + (','.join(self.next)) + ", prev=" + (','.join(self.prev)) + ")"

class Work(object):
    def __init__(self,c):
        self.code = c
        self.time = PENALTY + ord(c) - 64

#data = [pull(t) for t in test]
#PENALTY = 0
#WORKERS = 2
data = [pull(t) for t in live]
PENALTY = 60
WORKERS = 5

print data

vals = set()
for i in data:
    print i
    vals.add( i[0] )
    vals.add( i[1] )

graph = {}
for v in vals:
    graph[v] = Node(v)

for left,right in data:
    graph[left].next.append( right )
    graph[right].prev.append( left )

print graph

ready = set()
inprogress = []

# Remove a node from the nodes.

def eliminate(c):
    for k,v in graph.items():
        if c in v.prev:
            v.prev.remove( c )

# Find the first ready node.

def findfirst():
    rdy = list(ready)
    rdy.sort()
    for k in rdy:
        if not graph[k].prev:
            return k
    return None


# Find ready nodes.

for k,v in graph.items():
    if not v.prev:
        ready.add( k )

# Move ready nodes to inprogress.

def StartWork():
    while len(inprogress) < WORKERS:
        nxt = findfirst()
        if nxt:
            print "Starting ", nxt
            ready.remove( nxt )
            inprogress.append( Work(nxt) )
        else:
            break

StartWork()
for i in itertools.count():
    print "Time", i

# If there is still work to do, do it.

    if inprogress:
        still = []
        for n in inprogress:
            n.time -= 1
            print n.code, n.time
            if n.time:
                still.append( n )
            else:
                ready = ready.union( set( graph[n.code].next ) )
                eliminate( n.code )
        inprogress = still

    StartWork()
    if not ready and not inprogress:
        break

