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

sgrid = {}
dgrid = {}
moves = ''
for y, line in enumerate(data):
    if not line:
        continue
    elif line[0] == '#':
        for x, c in enumerate(line):
            sgrid[(x, y)] = c
            if c == 'O':
                dgrid[(x + x, y)] = '['
                dgrid[(x + x + 1, y)] = ']'
            elif c == '@':
                dgrid[(x + x, y)] = c
                dgrid[(x + x + 1, y)] = '.'
                srobot = (x, y)
                drobot = (x+x, y)
            else:
                dgrid[(x + x, y)] = c
                dgrid[(x + x + 1, y)] = c
    elif line:
        moves += line

def printgrid(grid):
    mw = max(k[0] for k in grid)+1
    mh = max(k[1] for k in grid)+1
    for y in range(mh):
        for x in range(mw):
            print(grid[(x, y)], end='')
        print()
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

def can_we_move(grid, pt, dir):
    dx, dy = dir
    affected = [pt]
    c = grid[pt]
    if dy:
        if c == '[':
            affected.append((pt[0] + 1, pt[1]))
        elif c == ']':
            affected.append((pt[0] - 1, pt[1]))

    for pt in affected:
        npt = (pt[0] + dx, pt[1] + dy)
        dc = grid[npt]
        if dc == '.':
            continue
        elif dc == '#':
            return False
        elif dc in 'O[]':
            if not can_we_move(grid, npt, dir):
                return False
    return True

def do_a_move(grid, pt, dir):
    if not can_we_move(grid, pt, dir):
        return False
    dx, dy = dir
    affected = [pt]
    c = grid[pt]
    if dy:
        if c == '[':
            affected.append((pt[0] + 1, pt[1]))
        elif c == ']':
            affected.append((pt[0] - 1, pt[1]))

    for pt in affected:
        c = grid[pt]
        npt = (pt[0] + dx, pt[1] + dy)
        dc = grid[npt]
        assert dc != '#'
        if dc == '.':
            grid[pt] = '.'
            grid[npt] = c
        elif dc in 'O[]':
            do_a_move(grid, npt, dir)
            grid[pt] = '.'
            grid[npt] = c
    return True


def part1(grid,robot,factor=1):
    bx, by = robot
    if DEBUG:
        print("START")
        printgrid(grid)
    for c in moves:
        dx,dy = dirs[c]
        if do_a_move(grid, (bx, by), (dx,dy)):
            bx += dx
            by += dy
            if grid[(bx, by)] != '@':
                printgrid(grid, factor)
                print(bx,by)
            assert grid[(bx,by)] == '@'
    if DEBUG:
        printgrid(grid)
    
    score = 0
    for k, v in grid.items():
        if v in 'O[':
            score += k[1] * 100 + k[0]
    return score

print("Part 1:", part1(sgrid,srobot,1))
print("Part 2:", part1(dgrid,drobot,2))