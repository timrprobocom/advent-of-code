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
#    data = open(day+'.txt').read()
    data = open(day+'.master').read()

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

def part1(codes):
    global allgates
    outgates = gates.copy()
    while codes:
        undone = []
        for a,op,b,_,r in codes:
            if a in outgates and b in outgates:
                outgates[r] = operate(outgates, a, op, b )
            else:
                undone.append((a,op,b,0,r))
        codes = undone
    allgates = list(outgates.keys())
    return binary(outgates, 'z')

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

#z[n] = xor(
#    xor(x[n], y[n]),
#    or(
#        and(x[n-1], y[n-1]),
#        and(
#            xor(x[n-1], y[n-1]),
#            ...
#        )
#    )
#)

#gwh jct rcb z09 z21 z39

def crack(codes):
    or_ins = {}
    xor_ins = {}
    and_ins = {}
    outs = {}
    for p in codes:
        outs[p[4]] = p
        if p[1] == 'AND':
            and_ins[p[0]] = p
            and_ins[p[2]] = p
        elif p[1] == 'OR':
            or_ins[p[0]] = p
            or_ins[p[2]] = p
        elif p[1] == 'XOR':
            xor_ins[p[0]] = p
            xor_ins[p[2]] = p

    zs = [f'z{i:02}' for i in range(46)]
    print(zs)

    # Make our expectations.

    swaps = []
    gates = {}
    for rzv in zs:
        gates['x'+rzv[1:]] = 0
        gates['y'+rzv[1:]] = 0
        sources = ['x'+rzv[1:],  'y'+rzv[1:]]
        new_rules = ["                  "] * 5
        while codes:
            undone = []
            for rule in codes:
                c1, op, c2, _, r = rule
                if c1 in gates and c2 in gates:
                    if op == 'AND':
                        gates[r] = gates[c1] & gates[c2]
                        if c1 in sources and c2 in sources:
                            new_rules[3] = ' '.join(rule)
                        else:
                            new_rules[2] = ' '.join(rule)
                    if op == 'OR':
                        gates[r] = gates[c1] | gates[c2]
                        new_rules[4] = ' '.join(rule)
                    if op == 'XOR':
                        gates[r] = gates[c1] ^ gates[c2]
                        if c1 in sources and c2 in sources:
                            new_rules[0] = ' '.join(rule)
                        else:
                            new_rules[1] = ' '.join(rule)
                            if r[0] != 'z':
                                print("WRONG", rule, 'swap', rzv, 'and', r )
                                swaps.append( rzv )
                                swaps.append( r )
                else:
                    undone.append( rule )
            if len(undone) == len(codes):
                break
            codes = undone
        if new_rules[0][-3:] not in new_rules[1]:
            print("WRONG", new_rules[0][-3:], 'not present in', new_rules[1])
        lastcarry = new_rules[-1][-3:]
        print(new_rules)
    print(swaps)


    return 1
        

    # Start at X1

    for i in range(1,45):
        x = f'x{i:02}'
        n1 = xor_ins[x]
        c1 = and_ins[x]
        print(n1,c1)
        z2 = xor_ins[n1[4]]
        p2 = and_ins[n1[4]]
        c2 = or_ins[c1[4]]
        print(i,i,i,n1,c1,z2,p2,c2)
        assert(z2[4][0] == 'z')
    return 0
exit(crack(codes))

def part2(codes,got):
    xx = binary(gates, 'x')
    yy = binary(gates, 'y')
    target = xx+yy
    diff = bin(target ^ got)[2:]
    print(target,got,target^got,diff)
    diffones = diff.count('1')
    wrong = []
    for i in range(len(diff)):
        if diff[-i-1] == '1':
            wrong.append(f'z{i:02}')
    print(wrong)
    badrules = []
    swaps = []
    for r in codes:
        if r[0] in wrong or r[2] in wrong or r[4] in wrong:
            badrules.append( r )
            if r[0][0] not in 'xy':
                swaps.append( r[0] )
            if r[2][0] not in 'xy':
                swaps.append( r[2] )
#            swaps.append(r[4])
    print(swaps)
    for b in badrules:
        print(b)
    return 1
    # For each pair of swaps, do we eliminate swapped bits in the result?

    maybe = set()
    for a,b in permutations(swaps,2):
        res = do_a_run(gates, codes, {a:b, b:a})
        if res:
            diffs = bin(target^res).count('1')
            if diffs < diffones:
                maybe.add((a,b))
    for a,b in maybe:
        print(a,b)

    res = do_a_run(gates, codes, maybe)
    print(target,res)
    return 0


p1 = part1(codes)
print("Part 1:", p1)
print("Part 2:", part2(codes,p1))
