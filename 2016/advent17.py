#
# Another backtracker.

import md5

directions = ( ('U',0,-1), ('D',0,1), ('L',-1,0), ('R',1,0) )  # U D L R

# Given a location, the passcode, and the path, make list of possible moves.

winner = ''

def move( x, y, path="" ):
    global winner
#    print x, y, path
    if x == 3 and y == 3:
        print "Success!", len(path), path
        if len(path) > len(winner):
            winner = path
        return

    md5x = md5.md5(code+path).hexdigest()[:4]

    for d,c in zip(directions,md5x):
        if 0 <= x+d[1] <= 3 and \
           0 <= y+d[2] <= 3 and \
           c >= 'b':
            move( x+d[1], y+d[2], path+d[0] )

#code = "hijkl"
#code = "ihgpwlah"
#code = "kglvqrro"
#code = "ulqzkmiv"
code = "qljzarfv"
move( 0, 0 )
print len(winner)
