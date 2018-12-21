#
#
#

import sys
import itertools

def addr(a, b):
    return reg[a]+reg[b]
def addi(a, b):
    return reg[a]+b

def mulr(a, b):
    return reg[a]*reg[b]
def muli(a, b):
    return reg[a]*b

def divi(a, b):
    return reg[a] // b
def divr(a, b):
    return reg[a] // reg[b]

def banr(a, b):
    return reg[a]&reg[b]
def bani(a, b):
    return reg[a]&b

def borr(a, b):
    return reg[a]|reg[b]
def bori(a, b):
    return reg[a]|b

def setr(a, b):
    return reg[a]
def seti(a, b):
    return a

def gtir(a,b):
    return 1 if a > reg[b] else 0
def gtri(a,b):
    return 1 if reg[a] > b else 0
def gtrr(a,b):
    return 1 if reg[a] > reg[b] else 0

def eqir(a,b):
    return 1 if a == reg[b] else 0
def eqri(a,b):
    return 1 if reg[a] == b else 0
def eqrr(a,b):
    return 1 if reg[a] == reg[b] else 0

# Opcodes where both must be registers.

opcodes = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
    "divi": divi,
    "divr": divr,
    "nop": None
}

program = []
pc = 0

for ln in sys.stdin:
    if ln[0] == '#':
        pc = int(ln[4:])
    else:
        i = ln.find('#')
        if i >= 0:
            ln = ln[:i]
        parts = ln.split()
        ops = (opcodes[parts.pop(0)],) + tuple(int(p) for p in parts)
        program.append( ops )

# Execute.

#for ln in program:
#    print ln

ends = set()

def run_to_end( r0=0 ):
    global reg
    reg = [r0,0,0,0,0,0]
    cycle = itertools.count()
    while reg[pc] < len(program):
        c = cycle.next()
        if c == 1000000:
            break
        if c % 10000 == 0:
            print '\r', c,
        opc,r1,r2,r3 = program[reg[pc]]
#    print opc,r1,r2,r3
        if opc:
            reg[r3] = opc(r1,r2)
        if reg[pc] == 28:
            print c, reg
            if reg[3] in ends:
                print "*** REPEAT"
                break
            ends.add( reg[3] )
        reg[pc] += 1
#        print c, reg
    return reg


#i = 10147168
i = 0
print "*************", i , "***************"
print run_to_end( i )


