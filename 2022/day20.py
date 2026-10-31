import sys

test = """\
1
2
-3
3
-2
0
4"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day20.txt').readlines()

DEBUG = 'debug' in sys.argv

def parse(data):
    return [[i,int(j)] for i,j in enumerate(data)]

def move(data, n):
    posn,delta = data[n]
    if delta < 0:
        delta += len(data) - 1

    newpos = (posn+delta) % (len(data)-1)
    if posn < newpos:
        for i in range(len(data)):
            if posn < data[i][0] <= newpos:
                data[i][0] -= 1
    elif posn > newpos:
        for i in range(len(data)):
            if newpos <= data[i][0] < posn:
                data[i][0] += 1
    data[n][0] = newpos

def result(data):
    # Find the value of the first item.
    zero = [pos for (pos, value) in data if value == 0][0]

    sumx = 0
    find = (
        (zero + 1000) % len(data),
        (zero + 2000) % len(data),
        (zero + 3000) % len(data)
    )

    for pos,val in data:
        if pos in find:
            yield val


def mix(data):
    for i in range(len(data)):
        move(data, i)

def part1(data):
    mix(data)
    return sum(result(data))

def part2(data):
    key = 811589153
    data = [[i,j*key] for i,j in data]
    for _ in range(10):
        mix(data)
    return sum(result(data))

print("Part 1:", part1(parse(data)))
print("Part 2:", part2(parse(data)))
