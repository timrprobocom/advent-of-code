import sys
import copy

live = [line for line in sys.stdin]

class Unit(object):
    def __init__(self,which,x,y):
        self.which = which
        self.x = x
        self.y = y
        self.hp = 200
    def __repr__(self):
        return '(Unit=%c at %d,%d hp=%d)' % (self.which,self.x,self.y,self.hp)
    def __cmp__(self,other):
        if self.y < other.y:
            return -1
        elif self.y == other.y:
            return self.x - other.x
        else:
            return 1


def makegrid(lines):
    grid = []
    units = []
    for y,ln in enumerate(lines):
        row = list(ln.strip())
        grid.append( row )
        for x,c in enumerate(row):
            if c in 'EG':
                units.append( Unit( c, x, y ) )
    return grid,units


def find( x, y ):
    for unit in units:
        if unit.x == x and unit.y == y:
            return unit
    return None

def printgrid(grid):
    for row in grid:
        print ''.join(row)

def find_attack( x, y, e ):
    picks = list(find(x+dx,y+dy) for dx,dy in moves if grid[y+dy][x+dx] == e)
    if picks:
        minhp = min(x.hp for x in picks)
        picks = list(x for x in picks if x.hp== minhp)
        return picks[0]
    return None



def find_target_cells( grid, unit ):
    # A target is an open cell adjacent to an enemy.

    mygrid = copy.deepcopy(grid)
    etype = other[unit.which]
    targets = []
    curr = [ [(unit.x,unit.y)] ]

    while not targets and curr:
        poss = []
        for path in curr:
            x,y = path[-1]

            tgt = find_attack( x, y, etype )
            if tgt:
                targets.append( path[1:] )
            
            # Check all 4 directions for new places.

            for dx,dy in moves:
                if mygrid[y+dy][x+dx] == '.':
                    poss.append( path + [(x+dx,y+dy)] )
                    mygrid[y+dy][x+dx] = 'x'

        curr = poss

    if not targets:
        return None

    if len(targets) > 1:
        # Choose the target whose first step occurs first in reading order.
        targets.sort( key=lambda k: (k[-1][1], k[-1][0], k[0][1],k[0][0]) )

    return targets[0]


moves = ((0,-1),(-1,0),(1,0),(0,1))
other = {'E':'G', 'G':'E'}
attack = {'E':3, 'G':3}


# For each player in reading order
#   Find the closest target cell
#   If distance==0 
#     Then attack
#   Else
#     Choose a direction to step
#     If now adjacent
#        Attack

def do_battle():
    rounds = 0
    all_done = False
    while any(u.which=='E' for u in units) and any(u.which=='G' for u in units):
        rounds += 1
#    printgrid(grid)
        units.sort()
#        for u in units:
#            print u
        remove = []
        for unit in units[:]:
            all_done = False
            if unit.hp <= 0:
                continue
            #print "Checking unit", unit
            etype = other[unit.which]

            enemy = find_attack( unit.x, unit.y, etype )
            if not enemy:
                # No one to attack, so go find a move to make.

                tgt =  find_target_cells( grid, unit )
                if not tgt:
                    continue

                #print "Found target", tgt
                top = tgt[0]

                # Take a step towards tgt[0],tgt[1]

                grid[unit.y][unit.x] = '.'
                grid[top[1]][top[0]] = unit.which
                unit.x = top[0]
                unit.y = top[1]

                enemy = find_attack( unit.x, unit.y, etype )

            if enemy:
                enemy.hp -= attack[unit.which]
                #print unit,'attacks',enemy
                if enemy.hp <= 0:
                    #print "Removing", enemy
                    grid[enemy.y][enemy.x] = '.'
                    units.remove( enemy )
                    if not len(list(u for u in units if u.which==enemy.which)):
                        all_done = True
                        print "**** DONE"

    return rounds if all_done else rounds-1

part = 1

for i in range(3,20):
    print "ATP", i
    attack['E'] = i
    grid,units = makegrid(live)
    elfcount0 = len(list(u for u in units if u.which=='E'))
    rounds = do_battle()
    printgrid(grid)
    elfcount1 = len(list(u for u in units if u.which=='E'))
    if elfcount0 == elfcount1:
        break
    else:
        print "Some elves died.", elfcount0, elfcount1
    if part==1 and i==3:
        break

sumx = 0
for u in units:
    print u
    sumx += u.hp
if any(u.which=='E' for u in units):
    print "Elves won"
else:
    print "Goblins won"
print rounds,sumx,rounds*sumx


