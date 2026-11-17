import sys

TEST = 'test' in sys.argv
DEBUG = 'DEBUG' in sys.argv

test = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

if TEST:
    data = test
else:
    data = open('day06.txt').read()
data = data.splitlines()

class Node(object):
    def __init__(self,me):
        self.me = me
        self.parent = ''
        self.child = []
        self.depth = 0

tree = {}
for s in data:
    a,b = s.strip().split(')')
    if a not in tree:
        tree[a] = Node(a)
    if b not in tree:
        tree[b] = Node(b)
    tree[a].child.append(b)
    tree[b].parent = a

xsum = 0

# Part 1

def count(st,depth):
    global xsum
    e = tree[st]
    e.depth = depth
    for i in e.child:
        count(i,depth+1)
        if DEBUG:
            print( st, ': After', i, ' now ', depth )
        xsum += depth + 1
    return xsum
    
def part1():
    return count('COM', 0)

# Part 2.

def getpath( el, path=[] ):
    cell = tree[el]
    if cell.parent:
        return getpath( cell.parent, path+[cell.parent] )
    return path

def part2():

    you = getpath('YOU')
    santa = getpath('SAN')
    equal = set(you).intersection(set(santa))

    if DEBUG:
        print( "Part 2: " )
        print( 'YOU:', len(you) )
        print( 'SANTA:', len(santa) )
        print( 'COMMON:', len(equal) )

# How many steps on the two branches that are not in common:

    return  len(you)-len(equal) + len(santa)-len(equal)

print( "Part 1:", part1() )
if not TEST:
    print( 'Part 2:', part2() )
