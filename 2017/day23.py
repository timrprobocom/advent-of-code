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
#set e 2
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
    'a':1,
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
    print registers
    registers['pc'] += 1

print muls
