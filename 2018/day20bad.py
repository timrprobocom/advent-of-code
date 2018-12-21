
#
#
#
from collections import defaultdict
import sys

rex = sys.stdin.read()
#rex = "^ENWWW(NEEE|SSE(EE|N))$"
#rex = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"

# First, produce the DAG.

def buildNodeEval(inp):
    to_python = inp.replace("^", "['").replace("$","']").replace("(","',[['") \
        .replace(")","']],'").replace("|","'],['").replace("[","(").replace("]",")")
    print( to_python )
    return eval(to_python)

def reader(sx):
    for c in sx:
        yield c

def parse(rdr):
    parts = []
    strx = ''
    for c in rdr:
        if c == '^':
            pass
        elif c == '(':
            if strx:
                parts.append(strx)
                strx = ''
            parts.append( parse(rdr ) )
        elif c == '|':
            if strx:
                parts.append(strx)
                strx = ''
            parts.append( parse(rdr ) )
            break
        elif c == ')':
            parts.append( strx )
            break
        elif  c == '$':
            parts.append( 0 )
            break
        else:
            strx += c
    if len(parts) == 1 and isinstance(parts[0],str):
        return parts[0]
    else:
        return tuple(parts)
     
#graph = buildNodeEval( rex )
graph = parse( reader(rex) )
print( graph )

# Now, depth first search to find lengths.
# First path is 11,036 long

# Remember each decision point with the fixed count up to that point?
# obj, count, idx?

# I need to have a function to pick up in the middle.  That is,
# given a nodelist, an index, an iteration number and a count,
# run from there out.

backtrack = []
lengths = []

class Node(object):
    def __init__(self, nodelist, idx, count ):
        self.nodes = nodelist
        self.index = idx
        self.count = count
        self.last = 0
    def advance(self):
        self.index += 1
        return self.index < len(self.nodes)
    def __repr__(self):
        return str((self.nodes,self.index,self.count,self.last))

def depthfirst( nodelist, idx, count ):
#    print( nodelist, idx, count )
#    if not nodelist:
#        lengths.append(count)
#        return count
    while idx < len(nodelist):
        if isinstance(nodelist[idx],str):
            count += len(nodelist[idx])
        elif not nodelist[idx]:
            return count
        else:
            backtrack.append( Node( nodelist, idx, count ) )
            count = depthfirst( nodelist[idx], 0, count )
        idx += 1
    return count

print( len(graph) )
print( depthfirst( graph, 0, 0 ) )
print (backtrack)

while backtrack:
    print( len(backtrack), end='\r')
    decpt = backtrack.pop()
    if decpt.advance():
        depthfirst( decpt.nodes, decpt.index, decpt.count )

print( lengths )
sys.exit(0)


dirx = { 'N': 0, 'E':1, 'S':0, 'W':-1 }
diry = { 'N': -1, 'E':0, 'S':1, 'W':0 }

adj = defaultdict(set)
def connect(a,b):
    global adj
    adj[a].add(b)
    adj[b].add(a)

# Make the adjacency map.

memo = {}
def traverse( pt, pieces ):
    key = (pt, pieces)
    if key in memo:
        return memo[key]
    
    positions = set([pt])

    for part in pieces:
        print( part )
        if isinstance(part, str):
            for c in part:
                newpositions = set()
                for pos in positions:
                    newpos = pos[0] + dirx[c], pos[1] + diry[c]
#                    print( pos, newpos )
                    connect( pos, newpos )
                    newpositions.add( newpos )
                positions = newpositions
        else:
            positions = set( k 
                for pos in positions 
                for choice in part
                for k in traverse( pos, choice )
            )

    memo[key] = positions
    return positions
              
traverse( (0,0), graph )
print( memo )
print( adj )

# Points we haven't looked at yet.
todo = [(0,0)]
distances = {}
dist = 0
while todo:
    newtodo = []
    for i in todo:
        if i in distances:
            continue
        distances[i] = dist
        newtodo.extend(adj[i])
    todo = newtodo
    dist += 1

print( distances )
print( max(distances.values()) )
