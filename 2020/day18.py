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

sys.exit( 0 )

def collapse( n, stack ):
    if not stack or stack[-1] == '(':
        stack.append( n )
    else:
        op = stack.pop()
        m = stack.pop()
        if op == '+':
            stack.append( m+n )
        else:
            stack.append( m*n )

def collapse2( stack ):
    n = stack.pop()
    stack.pop()
    stack[-1] *= n

def part1(expr):
    if DEBUG:
        print( "*** ", expr )
    stack = []
    for c in expr:
        if c == ' ':
            continue
        if c in '0123456789':
            n = ord(c) - ord('0')
            collapse( n, stack )
        elif c in '+*(':
            stack.append( c )
        elif c == ')':
            n = stack.pop()
            stack.pop()
            collapse( n, stack )
    return stack[0]

def part2(expr):
    if DEBUG:
        print( "*** ", expr )
    stack = []
    for c in expr:
        if c == ' ':
            continue
        if c in '0123456789':
            n = ord(c) - ord('0')
            if not stack or stack[-1] == '(':
                stack.append( n )
            elif stack[-1] == '+':
                collapse( n, stack )
            else:
                stack.append( n )
        elif c == '*':
            if len(stack) > 2 and stack[-2] == '*':
                collapse2( stack )
            stack.append( c )
        elif c in '+(':
            stack.append( c )
        elif c == ')':
            n = stack.pop()
            if stack[-1] == '*':
                stack.pop()
                n *= stack.pop()
            stack.pop()
            if stack and stack[-1] == '+':
                collapse( n, stack )
            else:
                stack.append( n )
        if DEBUG:
            print( c, stack )
    if len(stack) > 1:
        collapse2( stack )
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
