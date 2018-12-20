
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
#sys.exit(0)

# Now, depth first search to find lengths.
# First path is 11,036 long

# Remember each decision point with the fixed count up to that point?
# obj, count, idx?
rememberhere = []

def depthsum( node, count ):
    for n in node:
        if isinstance(n,str):
            count += len(n)
        elif isinstance(n,int):
            print count
            print "END"
            break
        else:
            rememberhere.append( [n, count, 0] )
    return count


print len(graph)
print depthsum(graph, 0)
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