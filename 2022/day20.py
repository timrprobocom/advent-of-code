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
    return [(i,int(j)) for i,j in enumerate(data)]

def move(data, i):
    # Find the item originally in position #i. 
    # position gives its current position.
    position, item = [
        (pos, item) for pos, item in enumerate(data) if item[0] == i
    ][0]

    data.pop(position)
    dest = (position + item[1]) % len(data)
    data.insert(dest, item)
    return data

def result(data):
    # Find the value of the first item.
    first = [i for (i, item) in enumerate(data) if item[1] == 0][0]
    for i in (1000, 2000, 3000):
        yield data[(first + i) % len(data)][1]

def mix(data):
    for i in range(len(data)):
        data = move(data, i)

def part1(data):
    data = parse(data)
    mix(data)
    return sum(result(data))

def part2(data):
    data = parse(data)
    key = 811589153
    data = [(i,j*key) for i,j in data]
    for _ in range(10):
        print('.',end='',flush=True)
        mix(data)
    print('',end='\r')
    return sum(result(data))

print("Part 1:", part1(data))
print("Part 2:", part2(data))
