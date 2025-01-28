import os
import sys
import itertools

test = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

WIDTH = len(data[0])
HEIGHT = len(data)

NORTH = (0,-1)
WEST = (-1,0)
SOUTH = (0,1)
EAST = (1,0)

def turn_right(pt):
    return (-pt[1],pt[0])

grid = []

GUARD = (-1,-1)

walkCounter = itertools.count()

originalPath = [ ]

class Cell:
    walkId = None
    blocked = False
    walked = {}
    def __init__(self):
        self.maybeResetCell(0)

    def maybeResetCell(self, walkid):
        if self.walkId != walkid:
            self.walkId = walkid
            self.walked = {d:False for d in (NORTH,SOUTH,EAST,WEST)}

def parseInput():
    global GUARD
        
    for row in range(HEIGHT):
        gridLine = []
        grid.append(gridLine)
        for col in range(WIDTH):
            cell = Cell()
            gridLine.append(cell)
            
            symbol = data[row][col]

            if symbol == '#':
                cell.blocked = True
            elif symbol == '^':
                GUARD = (col,row)

class PathCell:
    def __init__(self,row,col,dir):
        self.x = col
        self.y = row
        self.direction = dir
    def pt(self):
        return (self.x,self.y)

def add(pt1,pt2):
    return pt1[0]+pt2[0],pt1[1]+pt2[1]


# This is part 1.

def walkOriginalPath():
    gx, gy = GUARD
    dir = NORTH

    while True:
        originalPath.append( PathCell(gy, gx, dir))
        nx,ny = add((gx,gy),dir)
        if nx not in range(WIDTH) or ny not in range(HEIGHT):
            break
        if grid[ny][nx].blocked:
            dir = turn_right(dir)
        else:
            gx,gy = nx,ny

    return set((pt.x,pt.y) for pt in originalPath)


def walkCandidateMap(gx, gy, direction):

    currentWalk = next(walkCounter)

    while True:

# We keep walking until we find a block.

        nx,ny = add((gx,gy),direction)
        if nx not in range(WIDTH) or ny not in range(HEIGHT):
            break
        if not grid[ny][nx].blocked:
            gx,gy = nx,ny
            continue
        currentCell = grid[gy][gx]
        currentCell.maybeResetCell(currentWalk)
        if currentCell.walked[direction]:
            return 1
        currentCell.walked[direction] = True
        direction = turn_right(direction)
    return 0

# This is part 2.  Why is this so danged much faster than my original code?

def walkCandidateMaps():
    checked = set()
    checked.add( GUARD )
    countOfLoopPaths = 0
    while len(originalPath) > 1:
        previousCell = originalPath.pop(0)
        blockingCell = originalPath[0].pt()
        if blockingCell in checked:
            continue
        checked.add( blockingCell )
        grid[blockingCell[1]][blockingCell[0]].blocked = True
        countOfLoopPaths += walkCandidateMap(previousCell.x, previousCell.y, previousCell.direction)
        grid[blockingCell[1]][blockingCell[0]].blocked = False
    return countOfLoopPaths

parseInput()
print("Part 1:", len(walkOriginalPath()))
print("Part 2:", walkCandidateMaps())
