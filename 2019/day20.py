import os
import sys
import time
import itertools
import collections
from tools import Point


test = """\
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               
"""

test2 = """\
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
"""


movements = ( Point(0,-1),Point(0,1),Point(-1,0),Point(1,0) )


# Find the key points.


class Maze(object):
    def __init__(self,source):
        if not isinstance(source,str):
            source = source.read()
        maze = [ln for ln in source.splitlines()]

        self.maze = maze
        self.w = w = len(maze[3])
        self.h = h = len(maze)

        gates = {}
        paths = {}

        for y in range(h):
            for x in range(w):
                if maze[y][x] == '.':
                    for check in (
                        maze[y][x-2:x],
                        maze[y][x+1:x+3],
                        maze[y-2][x]+maze[y-1][x],
                        maze[y+1][x]+maze[y+2][x]
                    ):
                        if check.isalpha():
                            pt = Point(x,y)
                            print( check, pt )
                            if check in gates:
                                paths[pt] = gates[check]
                                gates[pt] = check
                                paths[gates[check]] = pt
                            else:
                                gates[check] = pt
                                gates[pt] = check

        self.gates = gates
        self.paths = paths
        self.start = self.gates['AA']
        self.goal = self.gates['ZZ']

        self.outer = set(pt for pt in paths if (pt.x in (2,w-3) or pt.y in (2,h-3)))
        self.inner = set(self.paths) - self.outer

    def __getitem__(self,pt):
        """ Allow indexing by a Point. """
        return self.maze[pt.y][pt.x]

    def bfs( self, part, start ):
        seen = set()
        unchecked = collections.deque()
        unchecked.append( (start,0,0) )
        lowerwalls = (self.start,self.goal)
        sec = int(time.time())
        while unchecked:
            pt,dist,level = unchecked.popleft()
            if TRACE and int(time.time()) != sec:
                sec = int(time.time())
                print( "Examine", pt, dist, level, len(unchecked) )
            if (pt,level) in seen:
                continue
            if pt == self.goal and level == 0:
                print( "GOAL" )
                return dist
            seen.add( (pt,level) )
            if pt in self.paths:
                newpt = self.paths[pt]
                newlvl = level
                if part == 2:
                    newlvl += 1 if pt in self.inner else -1
                if (newpt,newlvl) not in seen:
                    unchecked.append( (newpt,dist+1,newlvl) )
                    continue
            for move in movements:
                newpt = pt + move
                if newpt in self.outer and level == 0:
                    continue
                if (newpt,level) in seen:
                    continue
                if level > 0 and newpt in lowerwalls:
                    continue
                if self[newpt] == '.':
                    unchecked.append( (newpt,dist+1,level) )

TRACE = 'trace' in sys.argv

# Part 1.

if 'test' in sys.argv:
    maze = Maze(test)
else:
    maze = Maze(open('day20.txt'))

print( maze.start, maze.goal )
print( "Part 1:", maze.bfs(1, maze.start) )

# Part 2.

if 'test' in sys.argv:
    maze = Maze(test2)

print( "Part 2:", maze.bfs(2, maze.start) )
