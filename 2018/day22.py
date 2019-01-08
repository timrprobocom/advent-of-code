from __future__ import print_function
import sys

def empty(*args,**kwargs):
    pass

depth = 0
target = (0,0)

pprint = empty
dbgprint = empty
for arg in sys.argv[1:]:
    if arg == '-v':
        from pprint import pprint
        dbgprint = print
    elif not depth:
        depth = int(arg)
    elif not target[0]:
        target = (int(arg),0)
    else:
        target = (target[0],int(arg))


# Tim's data
if not depth:
    depth = 3339
    target = (10,715)

print( "depth=%d, target=(%d,%d)" % (depth, target[0], target[1]) )

# Test data:   510  10 10
# Bog's data:   6969  9 796

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

initial = (0,0,TORCH)
froms = { initial: None }

def checkpaths():
    cost = { initial: 0 }
    probes = { initial }
    mincost = 2500
    while probes:
        dbgprint( "New round" )
        newprobes = set()
        for x,y,tool in probes:
            dcost = cost[x,y,tool]
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
                froms[nx,ny,newtool] = (x,y,tool)

                if (nx,ny) == target:
                    if newcost < mincost:
                        mincost = newcost
                        mintool = newtool
                        print( "New min", mincost, file=sys.stderr )
                else:
                    newprobes.add((nx,ny,newtool))

        probes = newprobes

    return mincost, mintool

result,tool = checkpaths()

print( "Part 2:", result )

# Plot it.

finish = (tgtx,tgty,tool)

def iterate(lst,f):
    while f:
        yield f
        f = lst[f]

maxx = max(n[0] for n in iterate(froms,finish))
maxy = max(n[1] for n in iterate(froms,finish))

print( "Maxima:", maxx, maxy )


grid = []
for y in range(maxy+1):
    grid.append( [' '] * (maxx+1) )

for node in iterate(froms,finish):
    grid[node[1]][node[0]] = '#'

for y in grid:
    print( ''.join(y) )
