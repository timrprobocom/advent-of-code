import os
import re
import sys

test = """\
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".split('\n')

# I've made this way too complicated.

# 1: 26 437 12240 13632 sum 26335
# 2: 46 1445 669060 23340 sum 693891

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = open('day18.txt').read().split('\n')[:-1]

# Very clever cheat.

class M(int):
    def __sub__(self,y): return M(int(self)*y)
    def __add__(self,y): return M(int(self)+y)
    def __mul__(self,y): return M(int(self)+y)

print( "Part 1:", sum(eval(re.sub(r'(\d)',r'M(\1)', ln).replace('*','-'))                  for ln in data ))
print( "Part 2:", sum(eval(re.sub(r'(\d)',r'M(\1)', ln).replace('*','-').replace('+','*')) for ln in data ))

#sys.exit( 0 )

def collapse( n, stack ):
    if not stack or stack[-1] == '(':
        stack.append( n )
    else:
        if stack.pop() == '+':
            stack[-1] += n
        else:
            stack[-1] *= n

def collapseX( stack ):
    stack[-3:] = [stack[-1] * stack[-3]]


def collapse3( n, stack ):
    if stack and stack[-1] == '+':
        collapse( n, stack )
    else:
        stack.append( n )

def part1(expr):
    if DEBUG:
        print( "*** ", expr )
    stack = []
    for c in expr:
        if c == ' ':
            continue
        if c.isdigit():
            n = ord(c) - ord('0')
            collapse( n, stack )
        elif c in '+*(':
            stack.append( c )
        elif c == ')':
            n = stack.pop()
            stack.pop() # must be (
            collapse( n, stack )
    return stack[0]

def part2(expr):
    if DEBUG:
        print( "*** ", expr )
    stack = []
    for c in expr:
        if c == ' ':
            continue
        if c.isdigit():
            n = ord(c) - ord('0')
            collapse3( n, stack )
        elif c == '*':
            if len(stack) > 2 and stack[-2] == '*':
                collapseX( stack )
            stack.append( c )
        elif c in '+(':
            stack.append( c )
        elif c == ')':
            n = stack.pop()
            if stack[-1] == '*':
                stack.pop()
                n *= stack.pop()
            stack.pop() # must be (
            collapse3( n, stack )
        if DEBUG:
            print( c, stack )
    if len(stack) > 1:
        collapseX( stack )
    return stack[0]

sumx = 0
for ln in data:
    if not ln:
        continue
    value =  part1(ln)
    sumx += value
    if DEBUG:
        print( value )

print( "Part 1:", sumx )

sumx = 0
for ln in data:
    if not ln:
        continue
    value =  part2(ln)
    sumx += value
    if DEBUG:
        print( value )

print( "Part 2:", sumx )
