import sys

if 'test' in sys.argv:
    data = [s.rstrip() for s in open('day10test.txt').readlines()]
else:
    data = [s.rstrip() for s in open('day10.txt').readlines()]

DEBUG = 'debug' in sys.argv

def part1(data):
    X = 1
    t = 1
    sumx = 0
    for row in data:
        t += 1
        if t % 40 == 20:
            if DEBUG:
                print(t, X, t*X)
            sumx += t * X
        if row.startswith('addx'):
            X += int(row[5:])
            t += 1
            if t % 40 == 20:
                if DEBUG:
                    print(t, X, t*X)
                sumx += t * X
    return sumx

w = 40
h = 6

def part2(data):
    screen = []
    X = 1
    for row in data:
        t = len(screen)%w
        screen.append( '#' if abs(X-t) <= 1 else ' ' )
        if row.startswith('addx'):
            t = len(screen)%w
            screen.append( '#' if abs(X-t) <= 1 else ' ' )
            X += int(row[5:])
    assert(len(screen) == w*h)
    rows = []
    for i in range(0,w*h,w):
        rows.append( ''.join(screen[i:i+w]) )
    return '\n'.join( rows )

print("Part 1:", part1(data))
print("Part 2:\n"+part2(data))

