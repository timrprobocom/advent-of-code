import os
import sys

test = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test
else:
    data = open(day+'.txt').read()

charts = [c.splitlines() for c in data.split('\n\n')]

DEBUG = 'debug' in sys.argv

def compare_columns(chart,a,b):
    return sum(row[a] != row[b] for row in chart)

def compare_rows(chart,a,b):
    return sum(ca!=cb for ca,cb in zip(chart[a],chart[b]))

# 9 1 check 1   0 1
# 9 2 check 2   01 23
# 9 3 check 3   012 345
# 9 4 check 4   0123 4567
# 9 5 check 4   1234 5678
# 9 6 check 3   345 678 
# 9 7 check 2   56 78
# 9 8 check 1   7 8

def find_h_reflect(chart,target=0):
    W = len(chart[0])
    H = len(chart)
    for col in range(1,W):
        check = min(col, W-col)
        miss = sum( compare_columns(chart, col-1-i, col+i)
                    for i in range(check)
                )
        if miss == target:
            if DEBUG:
                print("H",col)
            return col
    return 0

def find_v_reflect(chart,target=0):
    W = len(chart[0])
    H = len(chart)
    for row in range(1,H):
        check = min(row, H-row)
        miss = sum( compare_rows(chart, row-i-1, row+i)
                    for i in range(check)     
                )
        if miss == target:
            if DEBUG:
                print("V",row)
            return row
    return 0

def part1(part,data):
    sumx = 0
    for chart in data:
        h = find_h_reflect(chart,part-1)
        v = find_v_reflect(chart,part-1)
        if DEBUG:
            print(h,v)
        sumx += 100*v+h
    return sumx

print("Part 1:", part1(1,charts))
print("Part 2:", part1(2,charts))
