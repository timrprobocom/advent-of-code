import sys
from dataclasses import dataclass

test = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2"""

if 'test' in sys.argv:
    idata = test.splitlines()
else:
    idata = open('day02.txt').readlines()

@dataclass
class Position:
    pos : int = 0
    depth : int = 0
    aim : int = 0

    def __repr__(self):
        return f"<Position {self.pos} {self.depth} {self.aim}>"

# Parse the directions.

data = []
for row in idata:
    parts = row.rstrip().split()
    data.append( (parts[0], int(parts[1])) )


def part1(data):
    pos = Position()
    for verb,cnt in data:
        if verb == 'forward':
            pos.pos += cnt
        elif verb == 'up':
            pos.depth -= cnt
        elif verb == 'down':
            pos.depth += cnt

    return pos.pos * pos.depth


def part2(data):
    pos = Position()
    for verb,cnt in data:
        if verb == 'forward':
            pos.pos += cnt
            pos.depth += pos.aim * cnt
        elif verb == 'up':
            pos.aim -= cnt
        elif verb == 'down':
            pos.aim += cnt

    return pos.pos * pos.depth

print("Part 1:", part1(data) )
print("Part 2:", part2(data) )

