import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

live = open('day7.txt').read()

if TEST:
    data = test.splitlines()
else:
    data = live.splitlines()

def parse(line):
    base = ''
    children = []
    for p in line.split():
        if p[-1] == ',':
            p = p[:-1]
        if not base:
            base = p
        elif p[0] == '(':
            weight = int(p[1:-1])
        elif p=='->':
            continue;
        else:
            children.append( p )
                
    return base, weight, children

progs = {}

for ln in data:
    base, wt, children = parse(ln)
    if base not in progs:
        progs[base] = { 'parent': None }
    progs[base]['weight'] = wt
    progs[base]['children'] = children
    for c in children:
        if c not in progs:
            progs[c] = {}
        progs[c]['parent'] = base

def part1(progs):
    for k,v in progs.items():
        if not v['parent']:
            return k

root = part1(progs)
print('Part 1:', root)

### Part 2, do a depth first traversal to establish weights

maxdepth = 0
def traverse( name, depth=0 ):
    global maxdepth
    if depth > maxdepth: maxdepth = depth
    node = progs[name]
    tot = node['weight']
    node['depth'] = depth
    for c in node['children']:
        tot += traverse( c, depth+1 )
    if node['children']:
        mn = min( progs[n]['total'] for n in node['children'] )
        mx = max( progs[n]['total'] for n in node['children'] )
        if mn != mx:
            if DEBUG:
                print(name, depth, tot, [progs[k]['total'] for k in node['children']])
            for i in node['children']:
                if progs[i]['total'] == mx:
                    if DEBUG:
                        print(i, "is", progs[i]['weight'], "should be", progs[i]['weight']-mx+mn)
                    progs['answer'] = progs[i]['weight']-mx+mn
                    progs[i]['total'] -= mx-mn
                    tot -= mx-mn
    node['total'] = tot
    return tot

traverse(root)
print('Part 2:', progs['answer'])

