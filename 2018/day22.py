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

depth = 3339
target = (10,715)

#depth = 510
#target = (10,10)

KY = 48271
KX = 16807
KMOD = 20183
PAD = 20

tgtx,tgty = target

# Build arrays.

erosion = []
types = []
row = list((x * KX + depth) % KMOD for x in range(tgtx+PAD) )
erosion.append( row )
types.append( list(x % 3 for x in row ) )
for y in range(1,tgty+PAD):
    row = [(y * KY + depth) % KMOD]
    line = []
    for x in range(1,tgtx+PAD):
        val = (row[x-1] * erosion[y-1][x] + depth) % KMOD
        row.append( val )
        line.append( val % 3 )
    erosion.append( row )
    types.append( list(x % 3 for x in row) )
erosion[tgty][tgtx] = erosion[0][0]
types[tgty][tgtx] = types[0][0]

encode = ".=|"
encode = "012"

for row in types:
    line = []
    for x in row:
        line.append( encode[x] )
    print( ''.join(line) )

print( "Part 1:", sum( sum( x for x in row[:tgtx+1] ) for row in types[:tgty+1] ) )

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


MX = 9999999
cost = []
for row in types:
    myrow = []
    for x in row:
        myrow.append( [MX,MX,MX] )
    cost.append(myrow)
cost[0][0] = [0,0,0]

def printcost(cost):
    for row in cost:
        dbgprint( ' '.join('%3d' % min(x) for x in row) )

printcost(cost)

def checkpaths():
    probes = [(0,0,TORCH)]
    mincost = 999999
    while probes:
        dbgprint( "New round" )
        newprobes = []
        for x,y,tool in probes:
            dcost = cost[y][x][tool]
            dbgprint( "Checking", x, y, "tool", tool, "cost", dcost )
            if dcost > mincost:
                continue
            for dx,dy in directions:
                nx = x+dx
                ny = y+dy
                dbgprint( "    ", nx, ny, end=' ' )
                if nx < 0 or ny < 0: 
                    dbgprint( "out of bounds" )
                    continue
                if nx >= len(cost[0]) or ny >= len(cost):
                    dbgprint( "out of bounds" )
                    continue
                dbgprint( types[ny][nx], "oldcost", dcost, end=' ' )

                # What would be the cost of moving here?

                if tool != types[ny][nx]:
                    # Yes, we can.
                    newcost = dcost+1
                    newtool = tool
                else:
                    dbgprint( "switch", end=' ' )
                    newcost = dcost+8
                    newtool = 3 - types[y][x] - types[ny][nx]

                if (nx,ny) == target:
                    if newtool != TORCH:
                        newcost += 7

                # Is this better than our last visit?

                if cost[ny][nx][newtool] <= newcost:
                    dbgprint( "no good" )
                    continue

                dbgprint( "now", newcost, "using", newtool )
                cost[ny][nx][newtool] = newcost

                if (nx,ny) == target:
                    if newcost < mincost:
                        mincost = newcost
                        print( "New min", mincost )
                else:
                    newprobes.append((nx,ny,newtool))

        printcost(cost)
        probes = newprobes
    return cost[tgty][tgtx]

result = checkpaths()

print( "Part 2:", result )
