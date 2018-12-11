#
#  Holy shit.
#

grid = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########""".splitlines()

xmax = len(grid[0])
ymax = len(grid)

# 0 is at row 18 col 3
# So, as long as there are no decisions, move forward.  When we reach a decision point,
# push the point on a stack, pick left, continue on.
# Stop when :
#  - no possible choices
#  - we hit all 8 numbers
#  - path is longer then the current shortest win
#  - we reach a visited point with the same collection of items
#
# Sheesh, one of the numbers is in a dead end, so we can't deny retracing.
# I suppose we can stop if we reach a point x with the same collection of items.

# Should preprocess to identify possible directions out of each point?

N,E,S,W = range(4)
deltas = ((-1,0),(0,1),(1,0),(0,-1))

def buildGrid( grid ):
    dgrid = []
    pills = {}
    for y in range(ymax):
        row = []
        for x in range(xmax):
            c = grid[y][x]
            if c == '#':
                row.append([])
            else:
                # Check N E S W
                works = []
                for dy,dx in deltas:
                    if  0 <= x+dx <= xmax and \
                        0 <= y+dy <= ymax and \
                        grid[y+dy][x+dx] != '#':
                        works.append( (dy,dx) )
                row.append( works )
                if c != '.':
                    pills[(y,x)] = c
        dgrid.append( row )
    return dgrid, pills

dgrid, pills = buildGrid( grid )

decisions = []

stack = []

class State(object):
    def __init__(self, x0, y0 ):
        self.x0 = x0
        self.y0 = y0
        self.came = None
        self.found = []
        self.path = []
        self.choices = ()

    def familiar(self):
        return (self.y0,self.x0,self.found) in self.path

    def update( self, pair ):
        self.path.append( (self.y0, self.x0, self.found) )
        self.y0 += pair[0]
        self.x0 += pair[1]

    def len(self):
        return len(self.path)

    def push(self):
        print "Pushing state"
        print self.path
        stack.append( self.__dict__.copy() )

    def pop(self):
        print "Popping state"
        dct = stack.pop()
        self.__dict__.update( dct )
        print self.path

def oneStep( s ):
    y0, x0 = s.y0, s.x0
    print "At ", y0, x0
    s.choices = dgrid[y0][x0][:]
    if (y0,x0) in pills:
        p = pills[(y0,x0)]
        if p not in s.found:
            print "Found ",  p
            s.found += p
            if len(s.found) == len(pills):
                print "*** found everything *** length ", s.len()
                s.pop()
                return
    if s.came:
        print "Came from ", s.came
        print "Choices are ", s.choices
        s.choices.remove( s.came )
    if len(s.choices) == 0:
        print "No more choices"
        s.pop()
        return
    if s.familiar():
        print "We've been here before."
        s.pop()
        return
    if len(s.choices) == 1:
        print "Must go ", s.choices[0]
        s.came = tuple(-k for k in s.choices[0])
        s.update( s.choices[0] )
        return
    s.push()
    pick = s.choices.pop(0)
    print "First choice ", pick
    s.came = tuple(-k for k in pick)
    s.update( pick )


state = State( 1, 1 );
state.push()
    
while 1:
    oneStep(state)

    
# Remember where we came from
# At each step:
#    Take list of choices
#    Remove from where we came
#    If there is only one remaining
#        Go that way
#    Otherwise
#        Remember x, y, treasures, 
#        for each possibility
#            Try it
