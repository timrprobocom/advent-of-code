import sys
from collections import Counter
from statistics import median

test = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day10.txt').readlines()

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

scores2 = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

def part1(data):
    score1 = 0
    score2 = []
    for line in data:
        line = line.rstrip()
        while True:
            found = False
            for pair in '[]','()','{}','<>':
                if pair in line:
                    line = line.replace(pair,'')
                    found = True
            if not found: 
                break
        l2 = line.lstrip('({[<')
        if l2:
            score1 += scores[l2[0]]
        else:
            sc = 0
            for c in line[::-1]:
                sc = sc * 5 + scores2[c]
            score2.append( sc )

    score2.sort()
    score2 = score2[len(score2)//2]

    return score1, score2

def printgrid(grid):
    for row in grid:
        for cell in row:
            print( "%5d"%cell, end = '')


score1,score2 = part1(data)
print("Part 1:", score1 )
print("Part 2:", score2 )
