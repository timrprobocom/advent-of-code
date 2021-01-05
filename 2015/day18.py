import sys

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

test = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####..""".splitlines()

if 'test' in sys.argv:
    size = 6
    cycles = 4
    data = test
else:
    size = 100
    cycles = 100
    data = open('day18.txt').read().splitlines()

master = []
for y,ln in enumerate(data):
    master.extend( [(x,y) for x,c in enumerate(ln) if c == '#'] )

neighbors = (
    (-1,-1), (-1, 0), (-1, 1),
    ( 0,-1),          ( 0, 1),
    ( 1,-1), ( 1, 0), ( 1, 1)
)

def neighborhood(lights, x, y):
    return sum( 1 for dx,dy in neighbors if (x+dx,y+dy) in lights )

def cycle(lights,force=[] ):
    new = set(force)
    for y in range(size):
        for x in range(size):
            nh = neighborhood( lights, x, y )
            if ((x,y) in lights and nh in (2,3)) or ((x,y) not in lights and nh==3):
                new.add( (x,y) )
    return new

lights = set(master)
for _ in range(cycles):
    lights = cycle(lights)
    dprint(len(lights))

print( "Part 1:", len(lights) )

force = [(0,0),(size-1,0),(size-1,size-1),(0,size-1)]

lights = set(master+force)
for _ in range(cycles):
    lights = cycle(lights,force)
    dprint(len(lights))

print( "Part 2:", len(lights) )

