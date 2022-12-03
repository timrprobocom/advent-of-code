import sys

test = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


if 'test' in sys.argv:
    vals = test.splitlines()
else:
    vals = [s.rstrip() for s in open('day03.txt').readlines()]

def part1(vals):
    prior = 0
    for row in vals:
        h = len(row)//2
        s1 = set(row[:h])
        s2 = set(row[h:])
        sect = list(s1.intersection(s2))[0]
        if sect > 'Z':
            prior += ord(sect)-ord('a')+1
        else:
            prior += ord(sect)-ord('A')+27
    return prior

def part2(vals):
    prior = 0
    counter = 2
    sect = None
    for row in vals:
        if sect:
            sect = sect.intersection(set(row))
        else:
            sect = set(row)
        if not counter:
            sect = list(sect)[0]
            if sect > 'Z':
                prior += ord(sect)-ord('a')+1
            else:
                prior += ord(sect)-ord('A')+27
            sect = None
            counter = 3
        counter -= 1
    return prior

print(part1(vals))
print(part2(vals))
