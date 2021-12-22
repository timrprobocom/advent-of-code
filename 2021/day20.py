import sys
import itertools

test = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day20.txt').readlines()

# Convert to a set of coordinates.

def convert(data):
    coords = set()
    for y,row in enumerate(data[2:]):
        for x,cell in enumerate(row):
            if cell == '#':
                coords.add( (x,y) )
    return coords

class Mapper:
    def __init__(self, data):
        self.algo = data[0]
        self.coords = convert(data)
        self.find_extrema()
        self.infinite = False

    def getval( self, x, y ):
        num = 0
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                num <<= 1
                if self.outside(x+dx,y+dy) or ((x+dx,y+dy) in self.coords):
                    num += 1
        return num

    def find_extrema(self):
        self.minx = min(x for x,y in self.coords)
        self.maxx = max(x for x,y in self.coords)
        self.miny = min(y for x,y in self.coords)
        self.maxy = max(y for x,y in self.coords)
        self.rangex = range(self.minx,self.maxx+1)
        self.rangey = range(self.miny,self.maxy+1)

    # In an evil twist, I (like many) did not realize that the entire infinite
    # background blinks with the live data, because algo[0] == '#' and algo[511] == '.'.
    # So, if a cell is out of bounds, return the state of the void.

    def outside(self,x,y):
        return self.infinite and (x not in self.rangex or y not in self.rangey)

    def printit(self):
        print("Grid:")
        for y in self.rangey:
            row = ['.#'[(x,y) in self.coords] for x in self.rangex]
            print(f"{y:3d}", ''.join(row))

    def generation(self):
        newcoords = set()
        for y in range(self.miny-1,self.maxy+2):
            for x in range(self.minx-1,self.maxx+2):
                if self.algo[self.getval(x,y)] == '#':
                    newcoords.add( (x,y) )
        self.infinite = self.algo[self.infinite*511] == '#'
        self.coords = newcoords
        self.find_extrema()

    def __len__(self):
        return len(self.coords)

def process(coords,n=2):
    if DEBUG:
        coords.printit()

    for _ in range(n):
        coords.generation()
        if DEBUG:
            coords.printit()
    return len(coords)

coords = Mapper(data)
print( "Part 1:", process(coords,2) )
print( "Part 2:", process(coords,48) )

