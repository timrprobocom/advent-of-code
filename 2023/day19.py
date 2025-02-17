import os
import sys
import re
import math

test = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

work,rating = data.split('\n\n')

match1 = re.compile(r"([xmas])=(\d+)")

parts = [
    {p1:int(p2) for p1,p2 in match1.findall(s) }
    for s in rating.splitlines()
]

match2 = re.compile(r'([xmas])([<>])(\d+):(\w+)')

flows = {}
for row in work.splitlines():
    name,work = row.split('{')
    steps = []
    for w in work.removesuffix('}').split(','):
        if ':' not in w:
            steps.append(w)
        else:
            g = match2.match(w)
            steps.append(g.groups())
    flows[name] = steps

DEBUG = 'debug' in sys.argv

# This seems ugly, but it's comparable to the other solutions.

def part1(parts,flows):
    sumx = 0
    for part in parts:
        phase = 'in'
        while phase not in 'RA':
            for step in flows[phase]:
                if isinstance(step,str):
                    phase = step
                    break
                xmas,cmpr,need,nextp = step
                val = part[xmas]
                need = int(need)
                if (cmpr == '<' and val < need) or (cmpr == '>' and val > need):
                    phase = nextp
                    break
        if phase == 'A':
            sumx += sum(part.values())
    return sumx

def copy(part):
    return { k: [v[0],v[1]] for k,v in part.items()}

def part2(flows):
    part = {'x':[1,4000],'m':[1,4000],'a':[1,4000],'s':[1,4000]}
    pending = [('in',part)]
    sumx = 0
    while pending:
        phase,part = pending.pop(0)
        if phase == 'A':
            sumx += math.prod( (v[1]-v[0]+1) for v in part.values() )
            continue
        if phase == 'R':
            continue
        for step in flows[phase]:
            if isinstance(step,str):
                pending.append( (step,part) )
                break
            xmas,cmpr,need,nextp = step
            need = int(need)

            # I originally had code to check for the condition where the
            # "need" value was completely above or below the range, but
            # it turns out that never happens.  EVERY rule splits a range.

            if cmpr == '<':
                #  x < 400   0,399   all take the jump
                #  x < 400   200,600 200..399 take the jump 400-600 move on
                #  x < 400   500,600 all move on
                p1 = copy(part)
                p1[xmas][1] = need-1
                pending.append((nextp,p1))
                part[xmas][0] = need
            else:
                #  x > 400   0,400   all move on
                #  x > 400   200,600 200..400 move on 401-600 take the jump
                #  x > 400   500,600 all take the jump
                p1 = copy(part)
                p1[xmas][0] = need+1
                pending.append((nextp,p1))
                part[xmas][1] = need

    return sumx

print("Part 1:", part1(parts,flows))
print("Part 2:", part2(flows))
