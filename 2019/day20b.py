import os
import sys
import itertools
import collections
from tools import Point


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

        self.outer = set(k for k in paths if isinstance(k,Point) and k.x < 5 or k.x > w-5 or k.y < 5 or k.y > h-5)
        self.inner = set(self.paths) - self.outer

    def __getitem__(self,pt):
        """ Allow indexing by a Point. """
        return self.maze[pt.y][pt.x]

    def bfs( self, start ):
        unchecked = collections.deque()
        unchecked.append( (start,[(start,0)], 0) )
        lowerwalls = (self.start,self.goal)
        while unchecked:
            pt,path,level = unchecked.popleft()
#            print( "Examine", pt, len(path), level )
#            if pt in self.doors:
#                print( "We're at", self.doors[pt], level )
#                print( path )
            if len(path) > 400:
                return -1
            if pt in self.paths:
                newpt = self.paths[pt]
                if (newpt,level) not in path:
                    unchecked.appendleft( (newpt,path+[newpt],level) )
            if pt == self.goal and level == 0:
                print( "GOAL" )
                print( path )
                return len(path) - 1
            for move in movements:
                newpt = pt + move
                if str.isupper(self[newpt]) and pt != start:
                    if self[newpt] == 'Z':
                        continue
                    newpt,delta = self.paths[newpt]
                    level += delta
                    if level < 0:
                        continue
#                print( newpt )
                if (newpt,level) in path or newpt.x < 2 or newpt.y < 2 or newpt.y >= self.h-2:
                    continue
                if level > 0 and newpt in lowerwalls:
                    continue
                elif self[newpt] == '.':
                    unchecked.append( (newpt,path+[(newpt,level)],level) )


#maze = Maze(open('day20.txt'))
maze = Maze(test2)
print("Inner",maze.inner)
print("Outer",maze.outer)
print( maze.start, maze.goal )
print( maze.bfs(maze.start) )
