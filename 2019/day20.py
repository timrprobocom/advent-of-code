import os
import sys
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



# The challenge will be to parse the maze.  After that, it's a BFS.

movements = ( Point(0,-1),Point(0,1),Point(-1,0),Point(1,0) )


# Find the key points.


class Maze(object):
    def __init__(self,source):
        if not isinstance(source,str):
            source = source.read()
        maze = [ln  for ln in source.splitlines()]

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

    def __getitem__(self,pt):
        """ Allow indexing by a Point. """
        return self.maze[pt.y][pt.x]

    def bfs( self, start ):
       unchecked = collections.deque()
       unchecked.append( (start,[start]) )
       while unchecked:
           pt,path = unchecked.popleft()
           if pt == self.goal:
               if TRACE:
                   print( "GOAL", path )
               return len(path) - 1
           if pt in self.paths:
               newpt = self.paths[pt]
               if newpt not in path:
                   unchecked.appendleft( (newpt,path+[newpt]) )
           for move in movements:
               newpt = pt + move
               if newpt in path or newpt.x < 2 or newpt.y < 2 or newpt.y >= self.h-2:
                   continue
               elif self[pt] == '.':
                   unchecked.append( (newpt,path+[newpt]) )

TRACE = 'trace' in sys.argv

if 'test' in sys.argv:
    maze = Maze(test)
else:
    maze = Maze(open('day20.txt'))

print( maze.start, maze.goal )
print( "Part 1:", maze.bfs(maze.start) )
