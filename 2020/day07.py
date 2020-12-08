import sys
from pprint import pprint

test = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".splitlines()

test2= """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".splitlines()

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = open('day07.txt').read().split('\n')[:-1]

def parse(data):
    rules = {}
    for ln in data:
        if DEBUG:
            print( ln )
        left,_,right = ln.partition(' bags contain ')
        rules[left] = []
        if right != 'no other bags.':
            for part in right.split(', '):
                count,w1,w2,_ = part.split()
                rules[left].append( (int(count),' '.join((w1,w2)) ) )
    return rules

rules = parse( data )
if DEBUG:
    pprint( rules )

# Does this bag contain the target?

def descend1( rules, bag, target ):
    return (bag == target) or any( descend1( rules, b[1], target) for b in rules[bag] )

target = 'shiny gold'

def part1( target ):
    return sum( key != target and descend1(rules,key,target) for key in rules.keys() )

print( "Part 1:", part1(target) )

# How many bags would this bag contain, not counting itself?

def contains( target ):
    return sum( count * (contains(bag) + 1) for count,bag in rules[target])

print( "Part 2:", contains(target) )
