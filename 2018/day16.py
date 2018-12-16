#
#
#

def addr(a, b):
    return reg[a]+reg[b]
def addi(a, b):
    return reg[a]+b

def mulr(a, b):
    return reg[a]*reg[b]
def muli(a, b):
    return reg[a]*b

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

opcodes = (
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr
)

def process( before, instr, after):
    global reg
    valid = set()
    for op in opcodes:
        reg = before[:]
        reg[instr[3]] = op(instr[1],instr[2])
        if reg == after:
            valid.add( op )
    return valid

live = 'day16.txt'

possibles = list(set(opcodes) for i in range(16))

before = []
instr = []
after = []
howmany = 0
for ln in open(live):
    if len(ln) < 2:
        continue
    if ln.startswith('Before:'):
        before = eval(ln[8:])
    elif ln.startswith('After:'):
        after = eval(ln[7:])
        matches = process( before, instr, after )
        if len(matches) > 3:
            howmany+=1
        possibles[instr[0]] = possibles[instr[0]].intersection(matches)
    else:
        instr = list(int(k) for k in ln.split())

print "Part 1:",  howmany

# Remove known opcodes from the possibles.

def eliminate_knowns(possibles):
    knowns = set(list(f)[0] for f in possibles if len(f)==1)
    for i in range(len(possibles)):
        if len(possibles[i]) > 1:
            possibles[i] = possibles[i].difference(knowns)

def anyleft(possibles):
    return any(f for f in possibles if len(f) > 1)

while anyleft(possibles):
    eliminate_knowns(possibles)

opcodes = list(f.pop() for f in possibles)
for i,f in enumerate(opcodes):
    print "Opcode",i,"is",f

# Part 2.

reg = [0,0,0,0]
for ln in open('day16b.txt'):
    instr = list(int(k) for k in ln.split())
    result = opcodes[instr[0]](instr[1],instr[2])
    reg[instr[3]] = result
print reg
print "Part 2:", reg[0]


