from collections import defaultdict
import sys

rex = sys.stdin.read()

# First, produce the DAG.

def buildNodeEval(inp):
    to_python = inp.replace("^", "['").replace("$","']").replace("(","',[['") \
        .replace(")","']],'").replace("|","'],['").replace("[","(").replace("]",")")
    print( to_python )
    return eval(to_python)

class DAG(object):
    ctr = 0
    def __init__(self, pfx="", parent=None):
        self.idx = DAG.ctr
        DAG.ctr += 1
        self.prefix = pfx
        self.next = []
    def __repr__(self):
        children = ','.join(str(k.idx) for k in self.next)
        return "Node(%d: '%s', next=[%s])" % (self.idx, self.prefix, children)

def reader(sx):
    for c in sx:
        yield c

def parse(rdr,parents):
    print( "parse", parents )
    tails = []
    strx = ''
    for c in rdr:
        if c == '(':
            # Create a node with strx as the prefix.
            # This node becomes the child of the last parent(s),
            # and the parent of the alternatives to follow.
            # Those alternatives become the parents of our next token.
            node = DAG(strx)
            strx = ''
            for n in parents:
                n.next.append( node )
            parents = parse( rdr, [node] )
            print( "( Parent now", parents )
        elif c == '|':
            # This is the first alternative.  All alternatives
            # share a single parent set.
            node = DAG(strx)
            strx = ''
            for n in parents:
                n.next.append( node )
            tails.append( node )
            print( "| Parent now", parents )
        elif c in ')$':
            # This is the final alternative.  Any dangling tails
            # become the new parents.
            node = DAG(strx)
            strx= ''
            for n in parents:
                n.next.append( node )
            print( ") Parent now", parents )
            tails += [node]
            break
        else:
            strx += c
    print( "Returning", tails, "as new parents" )
    return tails

allpaths = open('dags.txt','w')

lengths = []

def traverse( node, txt=''):
    if not node.next:
        lengths.append( len(txt) )
        if len(lengths) % 10000 == 0:
            print( len(lengths), end='\r' )
#        allpaths.write( txt+'\n' )
#        print( " >>> ", txt )
    for n in node.next:
        traverse( n, txt+n.prefix )
    

print( rex )
rdr = reader(rex)
c = next(rdr)
graph = DAG()
print( "Parsing..." )
parse( rdr, [graph] )
print( "Traversing..." )
traverse( graph )


print( lengths )
print( len(lengths) )
print( max(lengths) )

