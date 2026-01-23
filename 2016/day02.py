import sys
moves = """ULL
RRDDD
LURDL
UUUUD""".splitlines()

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if not TEST:
    moves = open('day2.txt').readlines()

pad1 = (
    '     ',
    ' 123 ',
    ' 456 ',
    ' 789 ',
    '     ' )

pad2 = (
    '       ',
    '   1   ',
    '  234  ',
    ' 56789 ',
    '  ABC  ',
    '   D   ',
    '       ')
    
def find5(pad):
    for y,line in enumerate(pad):
        if '5' in line:
            return line.index('5'),y
    return -1,-1

def part1(pad,moves):
    res = ''
    x,y = find5(pad)

    for ln in moves:
        for c in ln.strip():
            nx,ny = x,y
            if c=='R': nx += 1
            elif c=='U': ny -= 1
            elif c=='L': nx -= 1
            elif c=='D': ny += 1
            if pad[ny][nx] != ' ':
                x,y=nx,ny
        res += pad[y][x]
    return res

print('Part 1:', part1(pad1,moves) )
print('Part 2:', part1(pad2,moves) )

