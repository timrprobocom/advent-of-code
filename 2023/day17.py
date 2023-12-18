import os
import sys
import heapq

test = r"""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

DEBUG = 'debug' in sys.argv

grid = [[int(k) for k in row] for row in data.splitlines()]

if 'plot' in sys.argv:
    import matplotlib.pyplot as plt
    plt.imshow(grid, cmap='hot')
    plt.show()
    exit(0)

WID = len(grid[0])
HGT = len(grid)

N,E,S,W = (0,-1),(1,0),(0,1),(-1,0)

def backward(dir):
    return (-dir[0],-dir[1])
    
# This is a Dijkstra search.

def part1(grid,mind,maxd):
    # Accum cost, X, Y, direction.  Cost has to be first so the dijkstra pop
    # gets the best choice so far.
    points = [(0,0,0,(0,0))]
    seen = set()
    costs = {}
    # At each step, we can go 1 and turn, or 2 and turn, or 3 and turn.
    while points:
        cost, x, y, dir = heapq.heappop(points)
        # If we hit the exit, yahoo.
        if x == WID-1 and y == HGT-1:
            break
        # If we've been here before, bail.
        if (x, y, dir) in seen:
            continue
        seen.add((x,y,dir))
        # Check all possible directions.  We can't go the way we were going,
        # and we can't go back the way we came.
        for direction in (N,E,S,W):
            if direction == dir or direction == backward(dir):
                continue
            dcost = 0
            for distance in range(1,maxd+1):
                xx = x + direction[0] * distance
                yy = y + direction[1] * distance
                if xx in range(WID) and yy in range(HGT):
                    dcost += grid[yy][xx]
                    if distance < mind:
                        continue
                    newc = cost + dcost
                    newp = (xx,yy,direction)
                    # If we've been here before more cheaply, then skip it.
                    if newp in costs and costs[newp] < newc:
                        continue
                    costs[newp] = newc
                    heapq.heappush( points, (newc,xx,yy,direction))
    return cost
   
print("Part 1:", part1(grid,1,3))
print("Part 2:", part1(grid,4,10))
