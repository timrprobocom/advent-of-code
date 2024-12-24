import os
import sys
import math
from collections import defaultdict, Counter
from itertools import permutations, combinations

test = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

gates = {}
codes = []
for line in data.splitlines():
    if ':' in line:
        a,b = line.split(': ')
        gates[a] = int(b)
    elif '->' in line:
        codes.append( line.split() )

def operate(gates,a,op,b):
    if op == 'AND':
        return gates[a] & gates[b]
    elif op == 'OR':
        return gates[a] | gates[b]
    elif op == 'XOR':
        return gates[a] ^ gates[b]

def binary(gates,c):
    keys = sorted((k for k in gates if k[0] == c), reverse=1)
    sumx = 0
    for k in keys:
        sumx = sumx * 2 + gates[k]
    return sumx

def do_a_run(gates, codes, swap):
    xgates = {k:v for k,v in gates.items() if k[0] in 'xy'}
    while codes:
        undone = []
        for a,op,b,_,r in codes:
            if a in xgates and b in xgates:
                r = swap.get(r,r)
                xgates[r] = operate(xgates, a, op, b)
            else:
                undone.append((a,op,b,0,r))
        if len(undone) == len(codes):
            return None
        codes = undone
    return binary(xgates,'z')

# Parse the rules.

#// Xn XOR Yn => Mn
#// Xn AND Yn => Nn
#// Cn-1 AND Mn => Rn
#// Cn-1 XOR Mn -> Zn
#// Rn OR Nn -> Cn

def part1(codes, gates):

    zs = [p[4] for p in codes if p[4][0] == 'z']
    zs.sort()

    # Make our expectations.

    swaps = []
    lastcarry = 'xxx'
    outgates = {}
    xgates = {}
    for rzv in zs:
        x = 'x'+rzv[1:]
        y = 'y'+rzv[1:]
        sources = [x,y]
        xgates[x] = gates.get(x,None)
        xgates[y] = gates.get(y,None)
        new_rules = [['   ','   ','   ','  ','   ']]*5
        while codes:
            undone = []
            for rule in codes:
                c1, op, c2, _, r = rule
                if c1 in xgates and c2 in xgates:
                    if op == 'AND':
                        xgates[r] = xgates[c1] & xgates[c2]
                        if c1 in sources and c2 in sources:
                            new_rules[3] = rule
                        else:
                            new_rules[2] = rule
                    if op == 'OR':
                        xgates[r] = xgates[c1] | xgates[c2]
                        new_rules[4] = rule
                    if op == 'XOR':
                        xgates[r] = xgates[c1] ^ xgates[c2]
                        if c1 in sources and c2 in sources:
                            new_rules[0] = rule
                        else:
                            new_rules[1] = rule
                else:
                    undone.append( rule )
            if len(undone) == len(codes):
                break
            codes = undone

        # Capture the output.

        outgates[rzv] = xgates.get(rzv,0)
        if DEBUG:
            print(new_rules)

        # Validate the rules.

        if new_rules[1][0] != '   ':
            if new_rules[1][4][0] != 'z':
                if DEBUG:
                    print("WRONG", new_rules[1], 'swap', rzv, 'and', new_rules[1][4] )
                swaps.append( rzv )
                swaps.append( new_rules[1][4] )
            if new_rules[0][4] not in new_rules[1]:
                if new_rules[1][0] == lastcarry:
                    shd = new_rules[1][2]
                else:
                    shd = new_rules[1][0]
                if DEBUG:
                    print("WRONG", new_rules[0][4], 'not present in', new_rules[1], 'swap', new_rules[0][4], shd)
                swaps.append( new_rules[0][4] )
                swaps.append( shd )
        if new_rules[4]:
            lastcarry = new_rules[4][4]
    return binary(outgates,'z'), swaps
        
def part2(codes,gates,got,swap):
    xx = binary(gates, 'x')
    yy = binary(gates, 'y')
    target = xx+yy
    diff = bin(target ^ got)[2:]
    if DEBUG:
        print(target,got,diff)
    res = ','.join(sorted(swap))

    swaps = {}
    while swap:
        a = swap.pop(0)
        b = swap.pop(0)
        swaps[a] = b
        swaps[b] = a
    ans = do_a_run(gates, codes, swaps )
    if DEBUG:
        print(target,ans)
    assert ans == target
    return res

p1,p2 = part1(codes,gates)
print("Part 1:", p1)
if not TEST:
    print("Part 2:", part2(codes,gates,p1,p2))
