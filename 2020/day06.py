import sys

test = """\
abc

a
b
c

ab
ac

a
a
a
a

b"""


DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.split('\n\n')
else:
    data = open('day06.txt').read().split('\n\n')

sumx = sum( len(set(line.replace('\n',''))) for line in data )

print("Part 1:", sumx)

sumx = 0
for chunk in data:
    master = None
    for line in chunk.splitlines():
        if master is None:
            master = set(line)
        else:
            master = master.intersection(set(line))
    if DEBUG:
        print(len(master), master)
    sumx += len(master)

print("Part 2:", sumx)

