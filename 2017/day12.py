import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""".splitlines()

live = open( "day12.txt" ).readlines()

data = test if TEST else live

# This is a directed, but non-acyclic graph.

connx = {}
allx = set()

for ln in data:
    parts = ln.split()
    if DEBUG:
        print(parts)
    base = int(parts.pop(0))
    allx.add( base )
    if base not in connx:
        connx[base] = set([base])
    parts.pop(0)
    for other in parts:
        o = int(other.rstrip(','))
        if o not in connx:
            connx[o] = set([o])
        connx[base].add( o )
        connx[o].add( base )

def descend( node, seen ):
    for i in connx[node]:
        if i not in seen:
            seen.add(i)
            descend( i, seen )

groups = []
while allx:
    seen = set()
    head = allx.pop()
    allx.add( head )
    descend( head, seen )
    groups.append(seen)
    if DEBUG:
        print(head, len(seen))
    allx -= seen
    if DEBUG:
        print(allx)

print("Part 1:", len(groups[0]))
print("Part 2:", len(groups))
