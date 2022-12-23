import sys
from collections import defaultdict

test = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

if 'test' in sys.argv:
    data = test.splitlines()
    BOX = 4 
else:
    data = open('day23.txt').readlines()
    BOX = 50

DEBUG = 'debug' in sys.argv

def parse(data):
    spots = set()
    for y,row in enumerate(data):
        for x,col in enumerate(row):
            if col == '#':
                spots.add( (x,y) )
    return spots

direcs = [
    ((-1,-1),(0,-1),(1,-1)), # N
    ((-1, 1),(0, 1),(1, 1)), # S
    ((-1,-1),(-1,0),(-1,1)), # W
    (( 1,-1),( 1,0),( 1,1))  # #
]

neighbors = set()
for d in direcs:
    neighbors = neighbors.union( d )

def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

def close(xmap,elf,dirs):
    return sum(add(elf,d) in xmap for d in dirs)

def part1(data):
    xmap = parse(data)
    if DEBUG:
        plot(xmap)
    for rnd in range(10):
        proposed = defaultdict(list)
        newmap = set()
        for elf in xmap:
            if close(xmap, elf, neighbors) == 0:
                # Leave us alone??
                assert elf not in newmap
                newmap.add( elf )
                continue
            x0,y0 = 0,0
            for dirs in direcs:
                if close(xmap,elf,dirs) == 0:
                    x0,y0 = add(elf,dirs[1])
                    break
            else:
                assert elf not in newmap
                newmap.add( elf )
                continue

            proposed[(x0,y0)].append(elf)

        for k,v in proposed.items():
            if len(v) == 1:
                assert k not in newmap
                newmap.add( k )
            else:
                newmap = newmap.union( v )

        xmap = newmap
        if DEBUG:
            print('round',rnd+1)
            print(xmap)
            plot(xmap)
        direcs.append(direcs.pop(0))

    xmin = min(e[0] for e in xmap)
    xmax = max(e[0] for e in xmap)
    ymin = min(e[1] for e in xmap)
    ymax = max(e[1] for e in xmap)
    cnt = len(xmap)

    direcs.append(direcs.pop(0))
    direcs.append(direcs.pop(0))

    return (xmax-xmin+1)*(ymax-ymin+1) - cnt


def plot(xmap):
    xmin = min(e[0] for e in xmap)
    xmax = max(e[0] for e in xmap)
    ymin = min(e[1] for e in xmap)
    ymax = max(e[1] for e in xmap)
    plt = [['.']*(xmax-xmin+1) for _ in range(ymax-ymin+1)]
    for x,y in xmap:
        plt[y-ymin][x-xmin] = '#'
    for row in plt:
        print(''.join(row) )



def part2(data):
    xmap = parse(data)
    if DEBUG:
        plot(xmap)
    for rnd in range(1,10000):
        moved = False
        proposed = defaultdict(list)
        newmap = set()
        for elf in xmap:
            if close(xmap, elf, neighbors) == 0:
                # Leave us alone??
                newmap.add( elf )
                continue
            x0,y0 = 0,0
            for dirs in direcs:
                if close(xmap,elf,dirs) == 0:
                    x0,y0 = add(elf,dirs[1])
                    break
            else:
                newmap.add( elf )
                continue

            proposed[(x0,y0)].append(elf)

        for k,v in proposed.items():
            if len(v) == 1:
                moved = True
                newmap.add( k )
            else:
                newmap = newmap.union( v )

        if not moved:
            break
        xmap = newmap
        direcs.append(direcs.pop(0))

    if DEBUG:
        plot(xmap)
    return rnd


print("Part 1:", part1(data))
print("Part 2:", part2(data))
