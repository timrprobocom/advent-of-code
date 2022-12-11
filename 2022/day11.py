import sys

test = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day11.txt').readlines()]

DEBUG = 'debug' in sys.argv

class Monkey:
    divisor = 3
    factor = 1
    def __init__(self):
        self.items = []
        self.divisible = 0
        self.true = 0
        self.false = 0
        self.operation = None
        self.inspected = 0

    def __repr__(self):
        return f"{self.items}, {self.inspected}"

def createMonkeys(data,divisor):
    monkeys = []
    factor = 1
    Monkey.divisor = divisor
    for line in data:
        if not line:
            continue
        parts = line.split()
        if line.startswith('Monkey'):
            monkey = Monkey()
            monkeys.append( monkey )
        elif parts[0] == 'Starting':
            monkey.items = [int(k.rstrip(',')) for k in parts[2:]]
        elif parts[0] == 'Operation:':
            if parts[4] == '+':
                monkey.operation = lambda k,n=int(parts[5]): k+n
            elif parts[5] == 'old':
                monkey.operation = lambda k: k*k
            else:
                monkey.operation = lambda k,n=int(parts[5]): k*n
        elif parts[0] == 'Test:':
            monkey.divisible = int(parts[3])
            factor *= monkey.divisible
        elif parts[0] == 'If' and parts[1] == 'true:':
            monkey.true = int(parts[5])
        elif parts[0] == 'If' and parts[1] == 'false:':
            monkey.false = int(parts[5])
    Monkey.factor = factor
    return monkeys

def doround(monkeys):
    for m in monkeys:
        m.inspected += len(m.items)
        while m.items:
            worry = (m.operation(m.items.pop(0)) // Monkey.divisor) % Monkey.factor
            if worry % m.divisible:
                monkeys[m.false].items.append(worry)
            else:
                monkeys[m.true].items.append(worry)

def part1(data,divisor,count):
    monkeys = createMonkeys(data, divisor)
    for _ in range(count):
        doround(monkeys)
    allx = sorted([m.inspected for m in monkeys])
    return allx[-2]*allx[-1]

print("Part 1:", part1(data,3,20))
print("Part 2:", part1(data,1,10000))

