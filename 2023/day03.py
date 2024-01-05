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
def OK(c):
    return c.isdigit() or c=='.'

# Convert grid to list of numbers and symbols.

def convert(data):
    numbers = []
    symbols = []
    for y,line in enumerate(data):
        num = False
        for x,c in enumerate(line):
            if c.isdigit():
                if not num:
                    numbers.append( [x,y,0] )
                    num = True
                numbers[-1][2] += 1
            else:
                num = False
                if c != '.':
                    symbols.append( (x,y) )
    n2 = []
    for x,y,l in numbers:
        n2.append( (x, y, l, int(data[y][x:x+l])) )
    return n2,symbols

numbers, symbols = convert(data)

def part2(part,numbers,symbols):
    sumx = 0
    for sx,sy in symbols:
        nums = [v for dx,dy,l,v in numbers
                  if (dy-1 <= sy <= dy+1) and (dx-1 <= sx <= dx+l)]
        if part==1:
            sumx += sum(nums)
        elif len(nums) == 2:
            sumx += nums[0]*nums[1]
    return sumx

print("Part 1:", part2(1,numbers,symbols)) # 514969
print("Part 2:", part2(2,numbers,symbols)) # 78915902
