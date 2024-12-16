import os
import sys
import re
from collections import defaultdict
import numpy as np

test = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

test2 = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

WIDTH = HEIGHT = len(data[0])

sgrid = []
dgrid = []
moves = ''
for y, line in enumerate(data):
    if not line:
        continue
    elif line[0] == '#':
        srow = list(line)
        drow = []
        for x, c in enumerate(line):
            if c == 'O':
                drow.extend( ['[',']'])
            elif c == '@':
                drow.extend( ['@','.'] )
                srobot = (x, y)
                drobot = (x+x, y)
            else:
                drow.extend( [c,c] )
        sgrid.append(srow)
        dgrid.append(drow)
    elif line:
        moves += line

def printgrid(grid):
    for row in grid:
        print(''.join(row))
    print()

dirs = {
    '<': (-1, 0),
    '^': (0, -1),
    '>': (1, 0),
    'v': (0,1)
}

# We call ourselves recursively, because when moving vertically,
# the number of cells being affected can double:
#  ...[][]...
#  ....[]....
#  .....@....

def can_we_move(grid, x, y, dx, dy):
    affected = [(x,y)]
    c = grid[y][x]
    if dy:
        if c == '[':
            affected.append((x + 1, y))
        elif c == ']':
            affected.append((x - 1, y))

    for (x,y) in affected:
        nx,ny = x+dx, y+dy
        dc = grid[ny][nx]
        if dc == '.':
            continue
        elif dc == '#':
            return False
        elif dc in 'O[]':
            if not can_we_move(grid, nx, ny, dx, dy):
                return False
    return True

def do_a_move(grid, x, y, dx, dy):
    if not can_we_move(grid, x, y, dx, dy):
        return False
    affected = [(x,y)]
    c = grid[y][x]
    if dy:
        if c == '[':
            affected.append((x + 1, y))
        elif c == ']':
            affected.append((x - 1, y))

    for pt in affected:
        x,y = pt
        c = grid[y][x]
        nx,ny = (x + dx, y + dy)
        dc = grid[ny][nx]
        if dc == '#':
            printgrid(grid)
            print(affected)
            print(x,y,nx,ny)
        assert dc != '#'
        if dc == '.':
            grid[y][x] = '.'
            grid[ny][nx] = c
        elif dc in 'O[]':
            do_a_move(grid, nx, ny, dx, dy)
            grid[y][x] = '.'
            grid[ny][nx] = c
    return True

def part1(grid,robot):
    bx, by = robot
    if DEBUG:
        print("START")
        printgrid(grid)
    for c in moves:
        dx,dy = dirs[c]
        if do_a_move(grid, bx, by, dx,dy):
            bx += dx
            by += dy
            if grid[by][bx] != '@':
                printgrid(grid)
                print(bx,by)
            assert grid[by][bx] == '@'
    if DEBUG:
        printgrid(grid)
    
    score = 0
    for y,row in enumerate(grid):
        for x,c in enumerate(row):
            if c in 'O[':
                score += y * 100 + x
    return score

print("Part 1:", part1(sgrid,srobot))
print("Part 2:", part1(dgrid,drobot))
