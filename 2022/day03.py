import sys

test = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day03.txt').readlines()]

def score(setx):
    char = setx.pop()
    if char > 'Z':
        return ord(char)-ord('a')+1
    else:
        return ord(char)-ord('A')+27

def part1(data):
    prior = 0
    for row in data:
        h = len(row)//2
        s1 = set(row[:h]).intersection( set(row[h:]) )
        prior += score(s1)
    return prior

def part2(data):
    prior = 0
    counter = 2
    sect = None
    for row in data:
        if sect:
            sect.intersection_update(set(row))
        else:
            sect = set(row)

        if not counter:
            prior += score(sect)
            sect = None
            counter = 3
        counter -= 1
    return prior

print("Part 1:", part1(data))
print("Part 2:", part2(data))
