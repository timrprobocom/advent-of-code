import sys
import math
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

live = """\
set b 65
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
#sub g b
nop
#jnz g 2
nop
#set f 0
nop
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
#jnz f 2
nop
#sub h -1
nop
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23"""


#for b = 106500 to 123500 in steps of 17  (100 loops)
#   d = 2
#   for e = 2; e < b; e++
#       COUNT HERE
#
#   e ++
#   if b ==e


analyze = """\
    set b 65
    set c b
    jnz a A     # Part 2
    jnz 1 B     # Part 1

A   mul b 100       # Count this one
    sub b -100000
    set c b
    sub c -17000

B   set f 1
    set d 2
E   set e 2
D   set g d
    mul g e
#    sub g b     ### the next three instructions are unnecessary
#    jnz g 2     # if g is zero (meaning d*e == b) clear f
#    set f 0

    sub e -1
    set g e
    sub g b
    jnz g D     # loop until b == e which is 164998 loops
    sub d -1
    set g d
    sub g b
    jnz g E     # loop until b == d (one round) which is 164998 loops
#    jnz f 2     # if f is zero bump h which is not used
#    sub h -1

    set g b
    sub g c
    jnz g 2     # if b == c exit
    jnz 1 3

    sub b -17
    jnz 1 B"""

debug = """\
set b 65
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -99881
set c b
sub c -17119
set f 1
set d 106380
set e 2 
jnz 1 10
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23"""


registers = { 
    'a':0,
    'b':0,
    'c':0,
    'd':0,
    'e':0,
    'f':0,
    'g':0,
    'h':0,
    'pc': 0
}

def lookup(v):
    if v in registers:
        return registers[v]
    else:
        return int(v)

code = []
for ln in live.splitlines():
    if ln[0] != '#':
        code.append( ln.split() )

# This code computes the number of primes between b and c (inclusive).
# It tries all divisors from 2 to N.  So, for part 1, this just does
# this just one multiply per loop for (65-2) x (65-2) loops.  3969.

muls = 0
while registers['pc'] < len(code):
#    print registers['pc'], code[registers['pc']]
    parts = code[registers['pc']]
    if parts[0] == 'set':
        registers[parts[1]] = lookup(parts[2])
    elif parts[0] == 'sub':
        registers[parts[1]] -= lookup(parts[2])
    elif parts[0] == 'mul':
        registers[parts[1]] *= lookup(parts[2])
        muls += 1
    elif parts[0] == 'jnz':
        if lookup(parts[1]):
            registers['pc'] += lookup(parts[2])
            continue
    if DEBUG:
        print(registers)
    registers['pc'] += 1

print('Part 1:', muls)

# For part 2, it is computing the number of primes between 106500 and 123500
# in a very expensive manner.  This WOULD have been in register a, but that's
# an O(N^3) process.  So, we cheat.

start = int(code[0][2]) * int(code[4][2]) - int(code[5][2])
end = start - int(code[7][2])
step = -int(code[-2][2])
if DEBUG:
    print(start,end,step)

cnt = 0
#for i in range(106500,123501,17):
for i in range(start,end+1,step):
    for j in range(2,int(math.sqrt(i)+2)):
        if i % j == 0:
            cnt += 1
            break

print('Part 2:', cnt)
