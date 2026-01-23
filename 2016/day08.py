import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

data = [
'rect 3x2',
'rotate column x=1 by 1',
'rotate row y=0 by 4',
'rotate column x=1 by 1'
]

sx = 7
sy = 3


data = [k.strip() for k in open('day8.txt').readlines()]
sx = 50
sy = 6


class Screen():
    def __init__( self, sx, sy ):
        self.sx = sx
        self.sy = sy
        self.screen = [ ['.']*sx for i in range(sy) ]

    def rect(self,w,h):
        for row in range(h):
            for col in range(w):
                self.screen[row][col] = '*'

    def rotateRow( self,y, n ):
        self.screen[y] = self.screen[y][-n:] + self.screen[y][:-n]

    def rotateCol( self,x, n ):
        collect = [ self.screen[row][x] for row in range(sy) ]
        collect = collect[-n:] + collect[:-n]
        for row,c in enumerate(collect):
            self.screen[row][x] = c

    def render(self):
        for row in self.screen:
            print( ''.join(row) )
        print()

    def count(self):
        cnt = 0
        for row in self.screen:
            for c in row:
                if c == '*':
                    cnt += 1
        return cnt

def parse( screen, line ):
    words = line.split()
    if words[0] == 'rect':
        size = [int(k) for k in words[1].split('x')]
        screen.rect( size[0], size[1] )
    elif words[0] == 'rotate':
        row = int(words[2][2:])
        cnt = int(words[4])
        if words[1] == 'column':
            screen.rotateCol( row, cnt )
        elif words[1] == 'row':
            screen.rotateRow( row, cnt )
        else:
            print( "Unknown word", words )
    else:
        print( "Unknown word", words )

screen = Screen( sx, sy )
for line in data:
    if DEBUG:
        print( line )
    parse( screen, line )
    if DEBUG:
        screen.render()

print( 'Part 1:', screen.count() )
print( 'Part 2 (requires manual analysis):' )
screen.render()
