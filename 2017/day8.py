test = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""".splitlines()

live = open('day8.txt').readlines()

def process(data):
    registers = {}
    xmax = 0

    for ln in data:
        parts = ln.split()
        if parts[1] == 'inc':
            delta = 1
        else:
            delta = -1

        val = int(parts[2])
        if parts[0] not in registers:
            registers[parts[0]] = 0
        if parts[4] not in registers:
            registers[parts[4]] = 0

        left = registers[parts[4]]
        right = int(parts[6])
        if parts[5] == '<':
            doit = left < right
        elif parts[5] == '<=':
            doit = left <= right
        elif parts[5] == '>':
            doit = left > right
        elif parts[5] == '>=':
            doit = left >= right
        elif parts[5] == '==':
            doit = left == right
        elif parts[5] == '!=':
            doit = left != right
        if doit:
            registers[parts[0]] += delta * val
            if registers[parts[0]] > xmax:
                xmax = registers[parts[0]]
    return max(registers.values()), xmax

print process(test)
print process(live)
