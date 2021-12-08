import sys
from collections import Counter
from statistics import median

test = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day08.txt').readlines()

data = [row.partition(' | ') for row in data]
data = [(p1.split(),p2.split()) for p1,_,p2 in data]

def part1(data):
    lengths = Counter()
    for _,p2 in data:
        for word in p2:
            lengths[len(word)] += 1
    return lengths[2]+lengths[3]+lengths[4]+lengths[7]

def part2(data):
    sumall = 0
    for p1,p2 in data:
        p1 = [set(c) for c in p1]
        p2 = [set(c) for c in p2]

        codes = [None] * 10

        # Find the easy ones.

        for c in p1:
            if len(c) == 2:
                codes[1] = c
            elif len(c) == 3:
                codes[7] = c
            elif len(c) == 4:
                codes[4] = c
            elif len(c) == 7:
                codes[8] = c

        # Now classify the 6s (0, 6, 9).

        for c in p1:
            if len(c) == 6:
                if not codes[1].issubset(c):
                    codes[6] = c
                elif codes[4].issubset(c):
                    codes[9] = c
                else:
                    codes[0] = c

        # Now classify the 5s (2, 3, 5).

        for c in p1:
            if len(c) == 5:
                if c.issubset(codes[6]):
                    codes[5] = c
                elif codes[1].issubset(c):
                    codes[3] = c
                else:
                    codes[2] = c

        sumn = 0
        for digit in p2:
            sumn = sumn * 10 + codes.index(digit)
        if DEBUG:
            print(sumn)
        sumall += sumn
    return sumall

print("Part 1:", part1(data) )
print("Part 2:", part2(data) )
