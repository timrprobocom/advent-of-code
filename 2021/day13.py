import sys
import itertools

test = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day13.txt').readlines()

dots = set()
folds = []

for row in data:
    row = row.strip()
    if not row:
        continue
    if row.startswith('fold'):
        i = row.find('=')
        folds.append( (row[i-1], int(row[i+1:])) )
#        _,_,z = row.split()
#        a,b = z.split('=')
#        folds.append((a,int(b)))
    else:
        dots.add( tuple(int(a) for a in row.split(',')) )

def fold(grid, axis, coord):
    # So for fold x 5
    # x=6 becomes x=4
    new = set()
    for pt in grid:
        if axis == 'x':
            if pt[0] > coord:
                new.add( (coord+coord-pt[0], pt[1] ))
            else:
                new.add( pt )
        else:
            if pt[1] > coord:
                new.add( (pt[0], coord+coord-pt[1] ) )
            else:
                new.add( pt )
    return new

if DEBUG:
    print(dots)
    print(folds)

def part1(dots):
    grid = fold( dots, *folds[0] )
    return len(grid)

def render(dots):
    w = max( k[0] for k in dots )
    h = max( k[1] for k in dots )
    layout = [ [' ' for _ in range(w+1)] for _ in range(h+1)]
    for pt in dots:
        layout[pt[1]][pt[0]] = '*'
    return '\n' + ('\n'.join( ''.join(k) for k in layout ))

def part2(grid):
    for f in folds:
        grid = fold( grid, *f )
    return render(grid)

print("Part 1:", part1(dots))  #  724
print("Part 2:", part2(dots))  #  CPJBERUL
