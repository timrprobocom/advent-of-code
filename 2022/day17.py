import re
import sys
from functools import cmp_to_key

test = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

if 'test' in sys.argv:
    data = test
else:
    data = open('day17.txt').read().strip()

DEBUG = 'debug' in sys.argv

class Rock:
    def __init__(self, pts, x, y):
        self.points = set( [(px+x,py+y) for px,py in pts] )
        # left edge is 0, bot edge is 0
    def left(self):
        if min(px for px,py in self.points) > 0:
            self.points = set((px-1,py) for px,py in self.points)
    def right(self):
        if max(px for px,py in self.points) < 6:
            self.points = set((px+1,py) for px,py in self.points)
    def down(self):
        if min(py for px,py in self.points) > 0:
            self.points = set((px,py-1) for px,py in self.points)
    def up(self):
        self.points = set((px,py+1) for px,py in self.points)

    def top(self):
        return max(py for px,py in self.points)

    def bottom(self):
        return min(py for px,py in self.points)

    def __repr__(self):
        return '<'+','.join(f'({x},{y})' for x,y in self.points)+'>'

rocktypes = [
    [[0,0],[1,0],[2,0],[3,0]],
    [[1,2],[0,1],[1,1],[2,1],[1,0]],
    [[2,2],[2,1],[0,0],[1,0],[2,0]],
    [[0,3],[0,2],[0,1],[0,0]],
    [[0,1],[1,1],[0,0],[1,0]]
]

def makerock(kind, x, y ):
    return Rock( rocktypes[kind], x, y )

def plot(rocks):
    ymax = toprow(rocks)
    chart = [['.']*7 for _ in range(ymax+2)]
    for x,y in rocks:
        chart[ymax-y+1][x] = '#'
    for row in chart:
        print('|'+''.join(row)+'|')
    print('|-------|\n')

def collision( rock, rocks ):
    return rock.points & rocks

def toprow(rocks):
    return max(y for x,y in rocks)

def part1(data):
    n = len(data)
    rocks = set()
    step = 0
    for i in range(2022):
        print(i,end='\r')
        if i and DEBUG:
            plot(rocks)
        y = toprow(rocks) + 4 if rocks else 3
        rock = makerock(i%len(rocktypes), 2, y )
        while True:

            # Go left/right.

            code = data[step % n]
            step += 1
            if code == '<':
                rock.left()
            else:
                rock.right()
            if collision(rock,rocks):
                if code == '<':
                    rock.right()
                else:
                    rock.left()

            # Go down.

            if not rock.bottom():
                rocks |= rock.points
                break
            rock.down()
            if rocks and collision(rock,rocks):
                rock.up()
                rocks |= rock.points
                break

    return toprow(rocks)+1

def signature(rocks):
    maxy = toprow(rocks)
    return frozenset([(x,maxy-y) for x,y in rocks if maxy-y < 30])

BIG = 1000000000000

def part2(data):
    n = len(data)
    rocks = set()
    step = 0
    layers = 0
    seen = {}
    i = 0
    while i <= BIG:
        print(i,end='\r')
        y = toprow(rocks) + 4 if rocks else 3
        rt = i % len(rocktypes)
        rock = makerock(rt, 2, y )
        while True:

            # Go left/right.

            code = data[step % n]
            step += 1
            if code == '<':
                rock.left()
            else:
                rock.right()
            if rocks and collision(rock,rocks):
                if code == '<':
                    rock.right()
                else:
                    rock.left()

            # Go down unless we're already at bottom.

            if not rock.bottom():
                rocks |= rock.points
                break
            rock.down()
            if collision(rock,rocks):
                rock.up()
                rocks |= rock.points
                top = toprow(rocks)
                sig = (step%len(data), rt, signature(rocks))
                if not layers and sig in seen:
                    (oldt,oldy) = seen[sig]
                    dy = top - oldy
                    dt = i - oldt
                    print("cycle:", i,y,oldt,oldy,dt,dy)
                    cycles = (BIG-i)//dt
                    layers += cycles*dy
                    i += cycles*dt
                seen[sig] = (i,top)
                break
        i += 1

    if DEBUG:
        plot(rocks)
    return toprow(rocks)+layers

print("Part 1:", part1(data))
print("Part 2:", part2(data))
