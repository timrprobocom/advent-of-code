import sys
from collections import defaultdict

test2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

test1 = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

DEBUG = 'debug' in sys.argv

if 'test1' in sys.argv:
    data = test1.splitlines()
elif 'test2' in sys.argv:
    data = test2.splitlines()
else:
    data = open('day12.txt').readlines()

def makecaves(data):
    caves = defaultdict( list )
    for line in data:
        x,y = line.strip().split('-')
        if y != 'start':
            caves[x].append(y)
        if x != 'start':
            caves[y].append(x)
    return caves

def part(part,data):
    paths = 0

    # Node we are considering, path we've taken so far, True if we've 
    # been to a lower-case cave twice.
    untried = [('start', ['start'], part==1)]

    while untried:
        node, path, twice = untried.pop()

        for n in data[node]:
            if n == 'end':
                if DEBUG:
                    print(path+[n])
                paths += 1
            elif n == n.lower() and n in path:
                if not twice:
                    untried.append( (n, path+[n], True) )
            else:
                untried.append( (n, path+[n], twice) )

    return paths

caves = makecaves(data)
if DEBUG:
    print(caves)
print("Part 1:", part(1,caves) )   # 4378
print("Part 2:", part(2,caves) )   # 133621
