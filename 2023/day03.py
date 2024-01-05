import sys

test = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [x.strip() for x in open('day03.txt').readlines()]

DEBUG = 'debug' in sys.argv

if DEBUG:
    debug = print
else:
    debug = lambda x: None

W = range(len(data[0]))
H = range(len(data))

dirs = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
OK = '0123456789.'

# See if the number at x0,y0 is surrounded by anything other than dots.

def check(x0,y0,l):
    for y in (y0-1,y0+1):
        if y in H:
            for x in range(x0-1,x0+l+1):
                if x in W:
                    if data[y][x] not in OK:
                        return True
    return False

# How long is the number at position x?

def numdigits(row,x):
    l = 0
    while x+l in W and row[x+l].isdigit():
        l += 1
    return l

# This solution looks for the numbers, and checks if there are any symbols around it.

def part1(data):
    sumx = 0
    for y,row in enumerate(data):
        x = 0
        while x in W:
            l = numdigits(row,x)
            if l:
                if check(x,y,l):
                    debug("Y:"+row[x:x+l])
                    sumx += int(row[x:x+l])
                else:
                    debug("n:"+row[x:x+l])
            x += l + 1
    return sumx

# row[x] points to the middle of a number.  Extract the number.

def extract(row,x):
    while x-1 in W and row[x-1].isdigit():
        x -= 1
    l = numdigits(row,x)
    return int(row[x:x+l])

# This solution looks for the symbols, and checks if there are any numbers around it.
# Turns out that no number is adjacent to two symbols, so this code works for both
# passes.

def part2(data,part):
    sumx = 0
    for y,line in enumerate(data):
        for x,c in enumerate(line):
            if c not in OK:
                nums = set(
                     extract(data[y+dy],x+dx)
                     for dx,dy in dirs
                     if x+dx in W and y+dy in H and data[y+dy][x+dx].isdigit()
                )
                debug(nums)
                if part==1:
                    sumx += sum(nums)
                elif len(nums) == 2:
                    nums = list(nums)
                    sumx += nums[0]*nums[1]
    return sumx

print("Part 1:", part2(data,1))
print("Part 2:", part2(data,2))
