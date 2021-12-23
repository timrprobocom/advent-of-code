import re
import sys
import itertools
import numpy as np

test = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

live = """\
#############
#...........#
###A#C#B#A###
  #D#D#B#C#
  #########"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = live

# A = 1 per step
# B = 10 per step
# C = 100 per step
# D = 1000 per step
#
# Never stop outside a room
# Never enter a room unless it is final
# Once a pod stops, it is dead until it can enter its room.
#
# A pod moves at most twice: once out to a pause spot, once back.
#
# There are 7 pause spots: 0 1 3 5 7 9 10
# Homes are 2 4 6 8.
#

costs = {2:1,4:10,6:100,8:1000}

class Pod:
    def __init__(self,no,x,y):
        self.no = no
        self.x = x
        self.y = y
        self.cost = costs[no]
    def __repr__(self):
        return f"<Pod {self.no}: {self.x},{self.y}>"
        

# Do we track the 8 things instead?
# Ask the musical question, where can you go?
# Easier to ask, what are the possible moves for this pod?

def filled(pods):
    hall = [0]*11
    for p in pods:
        if p.y == 0:
            hall[p.x] = p.no
    return hall

def possibles(pod):
    # What are our possible spots, for pod 2?
    #  2,2 or 2,1 or 0 1 3 5 7 9 10

    otherpod = [p for p in podlist if p.no == pod.no and p.x != pod.x][0]

    filled = set(p.x for p in podlist if p.y==0)

    # Is home open?
    if homes[pod.no] == (0,0) or homes[pod.no] == [pod.no,0]:

        # Can we get home?

        if pod.x < pod.no:
            #  1  4
            r = range(pod.x+1,pod.no)
        else:
            #  9  2 
            r = range(pod.no+1, pod.x)
        if not any(i in filled for i in r):
            # Go home.
            return [pod.no]

    # Where can we go, left/right?

    poss = []
    m = pod.x-1
    while m >= 0:
        if m in filled:
            break
        poss.append(m)
        m -= 2 if m>1 else 1
    m = pod.x+1
    while m < 11:
        if m in filled:
            break
        poss.append(m)
        m += 2 if m<9 else 1
    return poss


homes = [ ('A','B'), ('D','C'),('C','B'),('A','D') ]
homes = [ 0, 0, (2,4), 0, (8,6), 0, (6,4),0, (2,8) ]
hallway = [0]*11

podlist = [
    Pod(2,2,2),
    Pod(2,8,2),
    Pod(4,2,1),
    Pod(4,6,1),
    Pod(6,4,1),
    Pod(6,6,2),
    Pod(8,4,2),
    Pod(8,8,1)
]

print(possibles(Pod(2,2,2)))

target = [ 0, 0, (2,2), 0, (4,4), 0, (6,6), 0, (8,8) ]

def move(pod,spot):
    # We're either moving out or moving home
    if spot == pod.no:
        if homes[pod.no] == (0,0):
            moves = abs(pod.no-pod.x) + 2
            homes[pod.no] = (pod.no,0)
            pod.x = pod.no
            pod.y = 2
        else:
            moves = abs(pod.no-pod.x) + 1
            homes[pod.no] = (pod.no,pod.no)
            pod.x = pod.no
            pod.y = 1
    else:
        if pod.y == 2:
            homes[pod.no] = (0,0)
        else:
            homes[pod.no] = (homes[pod.no][0],0)
        moves = pod.y + abs(spot-pod.x)
        pod.x = spot
        pod.y = 0

    return pod, moves * pod.cost



filled0 = set(p.x for p in podlist if p.y==0)
filled1 = set(p.x for p in podlist if p.y==1)
filled2 = set(p.x for p in podlist if p.y==2)
for pod in podlist:
    if pod.x == pod.no and pod.y == 2:
        continue
    if pod.y == 2 and pod.x in filled1:
        continue
    moves = possibles( pod )
    print( "Pod", pod.no, "moving to", moves )
    if moves:
        move( pod, moves[0] )

print( podlist)



# So, we need to generate the possible moves from a state.  We'll need to track seen states.

# If a pod can go home, take it home.  It could be in someone else's home


