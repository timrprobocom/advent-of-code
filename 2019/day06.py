test = (
'COM)B',
'B)C',
'C)D',
'D)E',
'E)F',
'B)G',
'G)H',
'D)I',
'E)J',
'J)K',
'K)L'
)


class Node(object):
    def __init__(self,me):
        self.me = me
        self.parent = ''
        self.child = []
        self.depth = 0

tree = {}

data = open('day06.txt').readlines()

for s in data:
    a,b = s.strip().split(')')
    if a not in tree:
        tree[a] = Node(a)
    if b not in tree:
        tree[b] = Node(b)
    tree[a].child.append(b)
    tree[b].parent = a

print( tree )

xsum = 0

# Part 1

def count(st,depth):
    global xsum
#    print( 'Checking', st )
    e = tree[st]
    e.depth = depth
#    print( len(e.child) )
    for i in e.child:
        count(i,depth+1)
        print( st, ': After', i, ' now ', depth )
        xsum += depth + 1
    return xsum
    

print( "Part 1: ", count('COM', 0))

# Part 2.

def getpath( el, path=[] ):
    cell = tree[el]
    if cell.parent:
        return getpath( cell.parent, path+[cell.parent] )
    return path

print( "Part 2: " )

you = getpath('YOU')
santa = getpath('SAN')
equal = set(you).intersection(set(santa))

print( 'YOU:', len(you) )
print( 'SANTA:', len(santa) )
print( 'COMMON:', len(equal) )

# How many steps on the two branches that are not in common:

print( 'Part 2:', len(you)-len(equal) + len(santa)-len(equal) )
