import sys
moves = """ULL
RRDDD
LURDL
UUUUD""".splitlines()


x,y = (2,2)

pad = ( '     ', ' 123 ', ' 456 ', ' 789 ', '     ' )

moves = open('../Downloads/day2.txt').readlines()
x,y = (4,4)
pad = (
    '       ',
    '   1   ',
    '  234  ',
    ' 56789 ',
    '  ABC  ',
    '   D   ',
    '       ')
    

for ln in moves:
    for c in ln.strip():
        nx,ny = x,y
        if c=='R': nx += 1
        elif c=='U': ny -= 1
        elif c=='L': nx -= 1
        elif c=='D': ny += 1
        if pad[ny][nx] != ' ':
            x,y=nx,ny

    print pad[y][x],

