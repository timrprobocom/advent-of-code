import sys
import math
import functools

DEBUG = 'debug' in sys.argv

data = open('day24.txt').readlines()

AX = []
DZ = []
AY = []
for lineno, line in enumerate(data):
    if "add x " in line and "add x z" not in line:
        AX.append(int(line.split()[2]))
    if "div z " in line:
        DZ.append(int(line.split()[2]))
    if "add y " in line and lineno%19 == 15:
        AY.append(int(line.split()[2]))

if DEBUG:
    print("Extracted from input")
    print("AX", AX)
    print("DZ", DZ)
    print("AY", AY)

assert len(AX) == 14
assert len(DZ) == 14
assert len(AY) == 14

stk = []
keys = []
for i,(ax,ay,dz) in enumerate(zip(AX,AY,DZ)):
    # if DZ is 1, then we push an element on the stack.
    if dz == 1:
        stk.append( (i,ay) )
    else:
        j,ayj = stk.pop()
        top = min(9, 9-ayj-ax)
        bot = max(1, 1-ayj-ax)
        keys.append( (j,bot,top) )
        keys.append( (i,10-top,10-bot) )
        
keys.sort()

xmin = 0
xmax = 0
for i,b,t in keys:
    xmin = xmin * 10 + b
    xmax = xmax * 10 + t

print( "Part 1:", xmax )
print( "Part 2:", xmin )


# -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8
#  9  9  9  9  9  9  9  9 9 8 7 6 5 4 3 2 1
#  9  8  7  6  5  4  3  2 1 1 1 1 1 1 1 1 1

# We get these constraints from the code itself.
#So dig[0]+14- 7 == dig[13]  +7 0 is 1,2
#So dig[1]+ 2-10 == dig[12]  -8 1 is 9
#So dig[2]+ 1- 5 == dig[11]  -4 2 is 5-9
#So dig[3]+13-12 == dig[6]   +1 3 is 1-8
#So dig[4]+ 5-12 == dig[5]   -7 4 is 8 9
#So dig[7]+ 9- 7 == dig[8]   +2 7 is 1-7
#So dig[9]+13- 8 == dig[10]  +5 9 is 1-4
