import os
import sys
import math
from collections import defaultdict
import heapq

test = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

test = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

test = """\
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

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

class Registers:
    A = 0
    B = 0
    C = 0
    P = 0
    def __str__(self):
        return str(self.__dict__)

registers = Registers()
program = []
for line in data.splitlines():
    line = line.strip()
    if line:
        words = line.split()
        if words[0] == 'Register':
            setattr(registers, words[1][0], int(words[2]))
        elif words[0] == 'Program:':
            program = [int(k) for k in words[1].split(',')]

def operand(n):
    if n < 4:
        return n
    if n in (4,5,6):
        return getattr(registers,'ABC'[n-4])
    assert n != 7

def adv(op):
    registers.A = registers.A // (2**op)
def bdv(op):
    registers.B = registers.A // (2**op)
def cdv(op):
    registers.C = registers.A // (2**op)
def bxl(op):
    registers.B = registers.B ^ op
def bst(op):
    registers.B = op & 7
def jnz(op):
    if registers.A:
        registers.P = op - 2
def bxc(op):
    registers.B = registers.B ^ registers.C
def out(op):
    return op & 7

ops = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
opc = "adv, bxl, bst, jnz, bxc, out, bdv, cdv".split(', ')

def run( program ):
    result = []
    while registers.P < len(program):
        i = program[registers.P]
        j = program[registers.P+1]
        if DEBUG:
            print(f"{registers.P} {i}={opc[i]} {j}={operand(j)} {registers}")
        k = ops[i]( j if i in (1,3) else operand(j))
        if k is not None:
            result.append(k)
        registers.P += 2
    return result

def part1(program):
    return ','.join(str(i) for i in run(program))

def step(A):
    B = (A & 7) ^ 3
    return B ^ (A >> B) ^ 5

def part2(program):
    # We start from the program, backwards, and find the values that create 
    # create the instruction for that step.  There might be several

    queue = list(range(8))
    for match in program[::-1]:
        # Run the program sequence for each potential A value.
        possible = [value for value in queue if step(value) & 7 == match]
        # Now produce the possible A values for the next digit.
        queue = [p*8+i for i in range(8) for p in possible]
    return min(possible)

print("Part 1:", part1(program))
if not TEST:
    print("Part 2:", part2(program))