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

        print( gates )
        print( paths )
        self.gates = gates
        self.paths = paths
        return




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
        inner = []
        outer = []
        # Tag, source, dest
        for y,ln in enumerate(self.maze):
            if ln[0:2] != '  ':
                outer.append( (ln[0:2], Point(1, y), Point(2, y) ) )
            if ln[-2:] != '  ':
                outer.append( (ln[-2:], Point(self.w-2, y), Point(self.w-3, y)))
            if ln[self.il] not in ' .#':
                inner.append( (ln[self.il:self.il+2], Point(self.il,y), Point(self.il-1, y)))
            if ln[self.ir] not in ' .#':
                inner.append( (ln[self.ir:self.ir+2], Point(self.ir+1,y), Point(self.ir+2, y)))
            if y in (0, self.it, self.ib, self.h-2):
                for x,ch in enumerate(ln):
                    if ch not in ' .#':
                        tag = ch + self.maze[y+1][x]
                        y0 = y+2 if y in (0,self.ib) else y-1
                        y1 = y+1 if y in (0,self.ib) else y
                        if y in (0, self.h-2):
                            outer.append( (tag, Point(x,y1), Point(x,y0)) )
                        else:
                            inner.append( (tag, Point(x,y1), Point(x,y0)) )
        self.inner = inner
        self.outer = outer

    def find_paths(self):
        doors = {}
        paths = {}
        for tag,pts,ptd in self.outer:
            doors[pts] = tag
            doors[ptd] = tag
            paths[tag] = (pts,ptd)
        for tag,pts,ptd in self.inner:
            xxs,xxd = paths[tag]
            paths[pts] = (xxd,-1)
            paths[xxs] = (ptd,1)
            paths[tag] += (pts,ptd)
        self.start = paths['AA'][1]
        self.goal = paths['ZZ'][1]
        self.paths = paths
        self.doors = doors
        return paths

    def bfs( self, start ):
       unchecked = collections.deque()
       unchecked.append( (start,[(start,0)], 0) )
       lowerwalls = (self.paths['AA'][0],self.paths['ZZ'][0])
       while unchecked:
           pt,path,level = unchecked.popleft()
#           print( "Examine", pt, len(path), level )
#           if pt in self.doors:
#               print( "We're at", self.doors[pt], level )
#               print( path )
           if len(path) > 400:
               return -1
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
#               print( newpt )
               if (newpt,level) in path or newpt.x < 2 or newpt.y < 2 or newpt.y >= self.h-2:
                   continue
               if level > 0 and newpt in lowerwalls:
                   continue
               elif self[newpt] == '.':
                   unchecked.append( (newpt,path+[(newpt,level)],level) )


#maze = Maze(open('day20.txt'))
maze = Maze(test2)
maze.find_gates()
print( 'Paths\n', maze.find_paths() )
print( 'Doors\n', maze.doors )
print( maze.start, maze.goal )
print( maze.bfs(maze.start) )
