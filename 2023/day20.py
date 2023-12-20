import os
import sys
import math
import collections

test = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

test2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test2.strip()
else:
    data = open(day+'.txt').read().strip()

DEBUG = 'debug' in sys.argv

class Part:
    def __init__(self,name,outputs):
        self.name= name
        self.inputs = {}
        self.outputs = outputs
        self.state = 0
    def addinput(self,inp):
        self.inputs[inp] = 0
    def reset(self):
        self.state = 0
    def input(self,inp,signal):
        return []
    def output(self,state):
        return [(self, o, state) for o in self.outputs]

class Broadcast(Part):
    def input(self):
        return self.output(0)

class FlipFlop(Part):
    def input(self,inp,signal):
        if not signal:
            self.state = 1 - self.state
            return self.output(self.state)
        return []

class Nand(Part):
    def reset(self):
        for k in self.inputs:
            self.inputs[k] = 0
    def input(self,inp,signal):
        self.inputs[inp] = signal
        return self.output(int(not all(self.inputs.values())))
    
circuit = {}
for row in data.splitlines():
    l,r = row.split(' -> ')
    if l == 'broadcaster':
        circuit[l] = Broadcast(l,r.split(', '))
    elif l[0] == '%':
        circuit[l[1:]] = FlipFlop(l[1:],r.split(', '))
    elif l[0] == '&':
        circuit[l[1:]] = Nand(l[1:],r.split(', '))

circuit['rx'] = Part('rx',[])

for name,part in circuit.items():
    for n in part.outputs:
        if n in circuit:
            circuit[n].addinput(name)

def part1(circuit):
    # Push da button
    circuit[0] = 0
    circuit[1] = 0
    
    for _ in range(1000):
        # Account for the button.
        circuit[0] += 1
        todo = circuit['broadcaster'].input()
        while todo:
            src,dst,state = todo.pop(0)
            circuit[state] += 1
            if dst in circuit:
                todo.extend( circuit[dst].input(src.name, state))
    if DEBUG:
        print(circuit[0],circuit[1])
    return circuit[0]*circuit[1]

def part2(circuit):

    # Reset the circuit.

    for p in circuit.values():
        if not isinstance(p,int):
            p.reset()

    # Now we have to find the cycles.
    # rx is fed by zh in my sample, and zh is fed by sx, jt, kb, ks.
    # rx only goes LOW (the target) when zh sends a HIGH, which only
    # happens when the four inputs go LOW.  So, find the cycles.

    check = list(circuit[list(circuit['rx'].inputs)[0]].inputs)
    if DEBUG:
        print(check)
    cycles = []
    prev = collections.defaultdict(list)
    t = 0
    while len(cycles) < 4:
        todo = circuit['broadcaster'].input()
        while todo:
            src,dst,state = todo.pop(0)                
            if dst in check and not state:
                if len(prev[dst]) == 1:
                    cycles.append( t - prev[dst][0] )
                prev[dst].append( t )
            todo.extend( circuit[dst].input(src.name, state))
        t += 1
    if DEBUG:
        print(cycles)
        print(prev)
    return math.prod(cycles)

print("Part 1:", part1(circuit))
if not 'test' in sys.argv:
    print("Part 2:", part2(circuit))
