import os
import sys
import math
from collections import defaultdict

test = ["""\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""",
"""\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""",
"""\
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""]

live = """\
Register A: 63687530
Register B: 0
Register C: 0

Program: 2,4,1,3,7,5,0,3,1,5,4,1,5,5,3,0"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = live

#       0    1    2    3    4    5    6    7
opc = "adv, bxl, bst, jnz, bxc, out, bdv, cdv".split(', ')

class CPU:
    A = 0
    B = 0
    C = 0
    P = 0

    def __init__(self, data):
        for line in data.splitlines():
            if line:
                words = line.split()
                if words[0] == 'Register':
                    setattr(self, words[1][0], int(words[2]))
                elif words[0] == 'Program:':
                    self.program = [int(k) for k in words[1].split(',')]

    def __str__(self):
        return str(self.__dict__)

    def adv(self, op):
        self.A = self.A // (2**self.combo(op))
    def bdv(self, op):
        self.B = self.A // (2**self.combo(op))
    def cdv(self, op):
        self.C = self.A // (2**self.combo(op))
    def bxl(self, op):
        self.B = self.B ^ op
    def bst(self, op):
        self.B = self.combo(op) & 7
    def jnz(self, op):
        if self.A:
            self.P = op - 2
    def bxc(self, op):
        self.B = self.B ^ self.C
    def out(self, op):
        return self.combo(op) & 7

    def ops(self,n):
        return [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv][n]

    def run(self):
        result = []
        while self.P < len(self.program):
            i = self.program[self.P]
            j = self.program[self.P+1]
            if DEBUG:
                print(f"{self.P} {i}:{opc[i]} {j}->{self.combo(j)} A={self.A} B={self.B} C={self.C}")
            k = self.ops(i)(j)
            if k is not None:
                result.append(k)
            self.P += 2
        return result

    def combo(self,n):
        assert n < 7
        match n:
            case 0 | 1 | 2 | 3:
                return n
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C

def part1(program):
    cpu = CPU(program)
    return ','.join(str(i) for i in cpu.run())

def part2(program):
    cpu = CPU(program)

    # The two variables here are the operands to the bxl statements.

    v = [cpu.program[i+1] for i in range(0,len(cpu.program),2) if cpu.program[i] == 1]

    def step(A):
        B = (A & 7) ^ v[0]
        return B ^ (A >> B) ^ v[1]

    # We start from the program, backwards, and find the values that create 
    # create the instruction for that step.  There might be several.

    queue = list(range(8))
    for match in cpu.program[::-1]:
        # Run the program sequence for each potential A value.
        possible = [value for value in queue if step(value) & 7 == match]
        # Now produce the possible A values for the next digit.
        queue = [p*8+i for i in range(8) for p in possible]

    # Verify.
    cpu.A = min(possible)
    assert cpu.program == cpu.run()

    return min(possible)

if TEST:
    for pgm in data:
        print("Part 1:", part1(pgm))
else:
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
