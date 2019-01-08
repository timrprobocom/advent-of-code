from __future__ import print_function
import sys

def empty(*args,**kwargs):
    pass

if '-v' in sys.argv:
    from pprint import pprint
    dbgprint = print
else:
    pprint = empty
    dbgprint = empty

# Tim's data
depth = 3339
target = (10,715)

# Test data
#depth = 510
#target = (10,10)

# Bog's data
depth = 6969
target = (9,796)

KY = 48271
KX = 16807
KMOD = 20183
PAD = 30

tgtx,tgty = target

# Build arrays.

class Cave(object):
    def __init__(self):
        self.erosion = {(0,0): depth, (tgtx,tgty): depth}
    def gete(self,x,y):
        if (x,y) in self.erosion:
            return self.erosion[x,y]
        if x == 0:
            e = (y * KY + depth) % KMOD
        elif y == 0:
            e = (x * KX + depth) % KMOD
        else:
            e = (self.gete(x-1,y) * self.gete(x,y-1) + depth) % KMOD
        self.erosion[x,y] = e
        return e
    def get(self,x,y):
        return self.gete(x,y) % 3


encode = ".=|"
encode = "012"

cave = Cave()

sumx = 0
for y in range(tgty+1):
    line = []
    for x in range(tgtx+1):
        line.append( encode[cave.get(x,y)] )
        sumx += cave.get(x,y)
    dbgprint( ''.join(line) )

print( "Part 1:", sumx )

# OK.
# Gear, torch, or nothing.
# Rocky (0)  = gear or torch.
# Wet (1) = gear or none.
# Narrow (2) = torch or none.
#
# 7 minutes to switch.
#
# At each step, we can choose any of the four directions.
# 

NONE,TORCH,GEAR = 0,1,2

directions = ( (0,-1), (-1,0), (1,0), (0,1) )

cost = {}
cost[0,0,0] = 0
cost[0,0,1] = 0
cost[0,0,2] = 0
paths = {}
paths[0,0,0] = [(0,0)]
paths[0,0,1] = [(0,0)]
paths[0,0,2] = [(0,0)]

def checkpaths():
    probes = {(0,0,TORCH)}
    mincost = 999999
    while probes:
        dbgprint( "New round" )
        newprobes = set()
        for x,y,tool in probes:
            dcost = cost[x,y,tool]
            path = paths[x,y,tool]
            dbgprint( "Checking", x, y, "tool", tool, "cost", dcost )
            if dcost >= mincost:
                continue
            for dx,dy in directions:
                nx = x+dx
                ny = y+dy
                dbgprint( "    ", nx, ny, end=' ' )
                if nx < 0 or ny < 0: 
                    dbgprint( "out of bounds" )
                    continue
                if nx >= tgtx+PAD or ny > tgty+PAD:
                    dbgprint( "out of bounds" )
                    continue
                newtype = cave.get(nx,ny)
                dbgprint( newtype, end=' ' )

                # What would be the cost of moving here?

                if tool != newtype:
                    # Yes, we can.
                    newcost = dcost+1
                    newtool = tool
                else:
                    dbgprint( "switch", end=' ' )
                    newcost = dcost+8
                    newtool = 3 - cave.get(x,y) - newtype

                if (nx,ny) == target and newtool != TORCH:
                    newcost += 7

                # Is this better than our last visit?

                if (nx,ny,newtool) in cost and cost[nx,ny,newtool] <= newcost:
                    dbgprint( "dead end" )
                    continue

                dbgprint( "now", newcost, "using", newtool )
                cost[nx,ny,newtool] = newcost
                paths[nx,ny,newtool] = path+[(nx,ny)]

                if (nx,ny) == target:
                    if newcost < mincost:
                        mincost = newcost
                        print( "New min", mincost )
                else:
                    newprobes.add((nx,ny,newtool))

        probes = newprobes

    # "min" would be just as good.
    return list(cost[tgtx,tgty,c] for c in range(3) if (tgtx,tgty,c) in cost)

result = checkpaths()

print( "Part 2:", min(result) )

# Plot it.

if (tgtx,tgty,1) in cost and cost[tgtx,tgty,1] > cost[tgtx,tgty,2]:
    path = paths[tgtx,tgty,1]
else:
    path = paths[tgtx,tgty,2]


maxx = max(p[0] for p in path )
maxy = max(p[1] for p in path )

print( "Maxima:", maxx, maxy )

grid = []
for y in range(maxy+1):
    grid.append( [' '] * (maxx+1) )

for x,y in path:
    grid[y][x] = '#'

for y in grid:
    print( ''.join(y) )
