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

        test = maze[h//2]

        for i in itertools.count(2):
            if test[i] not in '.#':
                self.il = i
                self.it = i
                break
        for i in itertools.count(w//2):
            if test[i] in '.#':
                self.ir = i-2
                break

        self.ib = h - (w - self.ir)

        print( w, h, self.il, self.ir, self.it, self.ib )

    def __getitem__(self,pt):
        """ Allow indexing by a Point. """
        return self.maze[pt.y][pt.x]

    def find_gates(self):
        gates = []
        # Tag, source, dest
        for y,ln in enumerate(self.maze):
            if ln[0:2] != '  ':
                gates.append( (ln[0:2], Point(1, y), Point(2, y) ) )
            if ln[-2:] != '  ':
                gates.append( (ln[-2:], Point(self.w-2, y), Point(self.w-3, y)))
            if ln[self.il] not in ' .#':
                gates.append( (ln[self.il:self.il+2], Point(self.il,y), Point(self.il-1, y)))
            if ln[self.ir] not in ' .#':
                gates.append( (ln[self.ir:self.ir+2], Point(self.ir+1,y), Point(self.ir+2, y)))
            if y in (0, self.it, self.ib, self.h-2):
                for x,ch in enumerate(ln):
                    if ch not in ' .#':
                        tag = ch + self.maze[y+1][x]
                        y0 = y+2 if y in (0,self.ib) else y-1
                        y1 = y+1 if y in (0,self.ib) else y
                        gates.append( (tag, Point(x,y1), Point(x,y0)) )
        self.gates = gates
        return gates

    def find_paths(self):
        doors = {}
        paths = {}
        for tag,pts,ptd in self.gates:
            doors[pts] = tag
            doors[ptd] = tag
            if tag in paths:
                xxs,xxd = paths[tag]
                paths[pts] = xxd
                paths[xxs] = ptd
                paths[tag] += (pts,ptd)
            else:
                paths[tag] = (pts,ptd)
        self.start = paths['AA'][1]
        self.goal = paths['ZZ'][1]
        self.paths = paths
        self.doors = doors
        return paths

    def bfs( self, start ):
       visits = set()
       unchecked = collections.deque()
       unchecked.append( (start,[start]) )
       while unchecked:
           pt,path = unchecked.popleft()
           visits.add(pt)
#           print( "Examine", pt, len(path) )
#           if pt in self.doors:
#               print( "We're at", self.doors[pt] )
#               print( path )
           if pt == self.goal:
               print( "GOAL" )
               print( path )
               return len(path) - 1
           for move in movements:
               newpt = pt + move
#               if newpt in visits:
#                   continue
               if str.isupper(self[newpt]) and pt != start:
                   newpt = self.paths[newpt]
               if newpt in path or newpt.x < 2 or newpt.y < 2 or newpt.y >= self.h-2:
                   continue
               elif self[pt] == '.':
                   unchecked.append( (newpt,path+[newpt]) )


maze = Maze(open('day20.txt'))
print( 'Gates\n', maze.find_gates() )
print( 'Paths\n', maze.find_paths() )
print( 'Doors\n', maze.doors )
print( maze.start, maze.goal )
print( maze.bfs(maze.start) )
