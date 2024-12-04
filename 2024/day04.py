import os
import sys

test = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').readlines()

data = list( l.strip() for l in data )
WIDTH = len(data[0])
HEIGHT = len(data)

# Find the Xes
def findall(c):
    xx = []
    for y,row in enumerate(data):
        for x,col in enumerate(row):
            if col==c:
                xx.append((x,y))
    return xx
               
dirs = ( (-1,-1), (-1,0), (-1,1),
         ( 0,-1),         (0,1),
         ( 1,-1), (1,0), (1,1))

def part1(data):
    winner = 0
    for x0,y0 in findall('X'):
        for dx,dy in dirs:
            x,y = x0,y0
            for c in 'MAS':
                x += dx
                y += dy
                if not (x in range(WIDTH) and y in range(HEIGHT) and data[y][x] == c):
                    break
            else:
                winner += 1
    return winner

def part2(data):
    winner = 0
    for x0,y0 in findall('A'):
        if not (0 < x0 < WIDTH-1) or not (0 < y0 < HEIGHT-1):
            continue
        if (
              (data[y0-1][x0-1] == 'M' and  data[y0+1][x0+1] == 'S') or 
              (data[y0-1][x0-1] == 'S' and  data[y0+1][x0+1] == 'M')
        ) and (
              (data[y0-1][x0+1] == 'M' and  data[y0+1][x0-1] == 'S') or 
              (data[y0-1][x0+1] == 'S' and  data[y0+1][x0-1] == 'M')
        ):
            winner += 1
    return winner

print("Part 1:", part1(data))
print("Part 2:", part2(data))