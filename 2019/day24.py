import itertools

inp="""\
...#.
#.##.
#..##
#.###
##..."""

test = """\
....#
#..#.
#..##
..#..
#...."""

grid = inp.splitlines()

def rating(grid):
    tot = 0
    for i,ln in enumerate(grid):
        for j,ch in enumerate(ln):
            if ch == '#':
                tot += 1 << (i*5+j)
    return tot



def cycle(grid):
    new = []
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            neighbors = 0
            for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)):
                if 0 <= x+dx < len(grid[0]) and \
                   0 <= y+dy < len(grid) and \
                    grid[y+dy][x+dx] == '#':
                    neighbors += 1
            if neighbors == 1 or (neighbors == 2 and grid[y][x] == '.'):
                row.append('#')
            else:
                row.append('.')
        new.append( ''.join(row) )
    return new

print( '\n'.join(grid))
print( rating( grid) )

values = {rating(grid): 0}
for i in itertools.count(1):
    grid = cycle(grid)
    print( '\n'.join(grid))
    r = rating(grid)
    print( i, r )
    if rating(grid) in values:
        print( r )
        break
    values[r] = i

print( "Part 1:", i, rating(grid) )


