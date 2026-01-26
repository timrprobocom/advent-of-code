#
# Another backtracker.

import sys
import hashlib

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv
directions = ( ('U',0,-1), ('D',0,1), ('L',-1,0), ('R',1,0) )  # U D L R

# Given a location, the passcode, and the path, make list of possible moves.

shortest = ''
longest = ''

def move( x, y, path="" ):
    global shortest
    global longest
#    print( x, y, path )
    if x == 3 and y == 3:
        if DEBUG:
            print( "Success!", len(path), path )
        shortest = path
        if len(path) > len(longest):
            longest = path
        return

    md5x = hashlib.md5((code+path).encode()).hexdigest()[:4]

    for d,c in zip(directions,md5x):
        if 0 <= x+d[1] <= 3 and \
           0 <= y+d[2] <= 3 and \
           c >= 'b':
            move( x+d[1], y+d[2], path+d[0] )

#code = "hijkl"
if TEST:
    code = "ihgpwlah"
    code = "kglvqrro"
    code = "ulqzkmiv"
else:
    code = "qljzarfv"
move( 0, 0 )
print('Part 1:', shortest)
print('Part 2:', len(longest))
