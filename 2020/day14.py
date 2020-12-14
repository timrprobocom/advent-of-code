import os
import sys
import functools
import itertools
import operator

test = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".splitlines()

test2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines()

from pprint import pprint

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = open('day14.txt').read().split('\n')[:-1]

def xlatemask1(mask):
    mask0 = value = 0
    for c in mask:
        mask0 <<= 1
        value <<= 1
        if c == 'X':
            mask0 += 1
        else:
            value += int(c)
    return mask0, value
        
def part1(data):
    memory = {}
    for ln in data:
        left,_,right = ln.split()
        if left == 'mask':
            mask0, value = xlatemask1(right)
            if DEBUG:
                print( hex(mask0), value )
        else:
            i = left.find('[')
            j = left.find(']')
            addr = int(left[i+1:j])
            val = int(right)
            if DEBUG:
                print( addr, val, (val & mask0) | value)
            memory[addr] = (val & mask0) | value

    if DEBUG:
        print( memory )
    return sum( memory.values() )


def xlatemask2(mask,addr):
    addr = ('0'*(len(mask)-len(addr)))+addr
    result = [a if m =='0' else m for m,a in zip(mask,addr)]
    return ''.join(result)


def nextaddr(mask):
    # Find all the X.  Produce all 0,1 combos for the Xs.
    allxs = [i for i,c in enumerate(mask) if c == 'X']
    substs = ["01"] * len(allxs)
    for pats in itertools.product(*substs):
        e1 = list(mask)
        for i,c in zip(allxs,pats):
            e1[i] = c
        yield int(''.join(e1),2)


def invert(addr):
    return addr ^ 0xfffffffff


def part2(data):

# Construct the list of floating memory writes.

    memory = []
    for ln in data:
        left,_,right = ln.split()
        if left == 'mask':
            mask = right
        else:
            i = left.find('[')
            j = left.find(']')
            addr = bin(int(left[i+1:j]))[2:]
            val = int(right)
            xm = xlatemask2(mask,addr)
            m,v = xlatemask1(xm)
            memory.append( (xm, invert(m), v, val) )
    if DEBUG:
        pprint( memory )
    
# For each write, for each variant of the address, if the address is not
# matched by a future write, add it to the sum.
# Can we encode the addresses more efficiently?  Maybe with ands/ors?

    return sum( 
        sum(pair[3] for addr in nextaddr(pair[0]) 
                    if not any( addr & mem[1] == mem[2] for mem in memory[i+1:]))
        for i,pair in enumerate(memory)
    )

    sumx = 0
    for i,pair in enumerate(memory):
        for addr in nextaddr(pair[0]):
            if not any( addr & mem[1] == mem[2] for mem in memory[i+1:]):
                sumx += pair[3]
    return sumx

# Part 1's test doesn't work in part 2.

print( "Part 1:", part1(data) )
if data != test:
    print( "Part 2:", part2(data) )
