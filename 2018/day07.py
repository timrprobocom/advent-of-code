
#
# Topological sort.
#

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
        self.data = c
        self.next = []
        self.prev = []
    def __repr__(self):
        return  "(next=" + (','.join(self.next)) + ", prev=" + (','.join(self.prev)) + ")"

data = [pull(t) for t in live]
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

# Find ready nodes.

for k,v in graph.items():
    if not v.prev:
        ready.add( k )

# Remove a node from the nodes.

def eliminate(c):
    for k,v in graph.items():
#        if c in v.next:
#            v.next.remove( c )
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

answer = ''
while ready:
#    print ready
    nxt = findfirst()
    answer += nxt
    print nxt
    ready = ready.union( set( graph[nxt].next ) )
    ready.remove( nxt )
    eliminate( nxt )

print answer
